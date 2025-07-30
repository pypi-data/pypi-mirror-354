from __future__ import annotations

import typing

import toolcache

from mince import dashboards
from mince import schemas

if typing.TYPE_CHECKING:
    import polars as pl
    from mince import types


@toolcache.cache(cachetype='memory', hash_include_args=['state'])
def _prepare_time_series_data(
    df: pl.DataFrame,
    state: dict[str, typing.Any],
    ui_spec: types.UiSpec,
) -> pl.DataFrame:
    import polars as pl
    import tooltime

    # filter end of timerange
    now = tooltime.timestamp_to_seconds(state['now'])
    df = df.filter(pl.col.timestamp.cast(pl.Int64) <= now * 1_000)

    # filter by metric
    df_metric = dashboards.get_df_metric(state, ui_spec)
    df = df.filter(pl.col.metric == df_metric)

    # aggregate by irrelevant dimensions
    df = _aggregate_by_irrelevant_dimensions(
        df,
        state,
        ui_spec['schema']['columns'],
        ui_spec,
    )

    # aggregate by time interval
    df = _aggregate_by_interval(df, state)

    # add age column
    if state['xalign'] == 'age':
        df = _add_age(df, state)

    # get cumulative value from t=0
    if (
        state['cumulative'] == 'cumulative (t=0)'
        and ui_spec['metrics'][df_metric]['type'] == 'sum'
    ):
        df = df.sort('timestamp').with_columns(
            value=pl.cum_sum('value').over(
                [
                    col
                    for col in schemas.get_series_columns(
                        ui_spec['schema']['columns']
                    )
                    if col != 'value' and col in df
                ]
            )
        )

    # filter by date range
    df = _filter_by_time_range(df, state)

    # get cumulative value from inside window
    if (
        state['cumulative'] == 'cumulative (window)'
        and ui_spec['metrics'][df_metric]['type'] == 'sum'
    ):
        df = df.sort('timestamp').with_columns(
            value=pl.cum_sum('value').over(
                [
                    col
                    for col in schemas.get_series_columns(
                        ui_spec['schema']['columns']
                    )
                    if col != 'value' and col in df
                ]
            )
        )

    # format-specific transformations
    if state['format'] == 'line':
        if state['total'] == 'total':
            df = _add_total_entry(df, state)
        if state['ynormalize'] == 'relative':
            df = _convert_to_relative(df, state)
    elif state['format'] == 'line %':
        df = _convert_to_percent(df, state)
    elif state['format'] == 'area':
        pass
    elif state['format'] == 'area %':
        df = _convert_to_percent(df, state)
    else:
        raise Exception('invalid format')

    # sort data
    df = _sort_data(df, state)

    return df


def _aggregate_by_irrelevant_dimensions(
    df: pl.DataFrame,
    state: dict[str, typing.Any],
    schema: dict[str, types.ColumnType],
    ui_spec: types.UiSpec,
) -> pl.DataFrame:
    import polars as pl

    agg_columns = [
        column for column in ui_spec['groupings'] if column != state['grouping']
    ]

    return (
        df.group_by(
            [col for col in df.columns if col not in agg_columns + ['value']],
            maintain_order=True,
        )
        .agg(pl.sum('value'))
        .with_columns(
            *[pl.lit('all').alias(agg_column) for agg_column in agg_columns]
        )
        .select(list(schema.keys()))
    )


def _aggregate_by_interval(
    df: pl.DataFrame, state: dict[str, typing.Any]
) -> pl.DataFrame:
    import polars as pl

    if len(df) == 0:
        raise Exception('empty dataframe')

    available_intervals = list(df['interval'].unique())

    if state['sample_interval'] == 'date':
        if 'day' in available_intervals:
            return df.filter(pl.col.interval == 'day')
        elif 'point' in available_intervals:
            return df.filter(pl.col.interval == 'point')
        else:
            raise Exception('date-level data not available')
    elif state['sample_interval'] in ['week', 'month']:
        if state['sample_interval'] in available_intervals:
            return df.filter(pl.col.interval == state['sample_interval'])
        else:
            # add sample_interval column
            if state['sample_interval'] == 'week':
                unix_seconds = pl.col.timestamp.cast(pl.Int64) / 1_000
                unix_week = ((unix_seconds + 4 * 86400) / 86400 / 7).floor()
                week = (unix_week * 86400 * 7 * 1_000 - 4 * 86400 * 1_000).cast(
                    pl.Datetime('ms')
                )
                df = df.with_columns(week=week)
            elif state['sample_interval'] == 'month':
                df = df.with_columns(month=pl.col.timestamp.dt.month_start())
            else:
                raise Exception('invalid sample interval')

            # perform aggregation
            group_columns = [
                state['grouping'],
                state['sample_interval'],
                'interval',
            ]
            if 'day' in available_intervals:
                return (
                    df.filter(pl.col.interval == 'day')
                    .group_by(group_columns, maintain_order=True)
                    .agg(pl.sum('value'))
                    .with_columns(
                        pl.col(state['sample_interval']).alias('timestamp'),
                        interval=pl.lit(state['sample_interval']),
                    )
                )
            elif 'point' in available_intervals:
                return (
                    df.filter(pl.col.interval == 'point')
                    .group_by(group_columns, maintain_order=True)
                    .agg(pl.first('value'))
                    .with_columns(
                        pl.col(state['sample_interval']).alias('timestamp'),
                    )
                )
            else:
                raise Exception('date-level data not available')
    else:
        raise Exception('invalid interval: ' + str(state['sample_interval']))


def _add_age(df: pl.DataFrame, state: dict[str, typing.Any]) -> pl.DataFrame:
    import polars as pl

    x = 'timestamp'
    raw_new_time_index = df[[x]].unique(x).sort(x).with_row_index()
    new_time_index = dict(raw_new_time_index[[x, 'index']].rows())

    group_starts = (
        df.group_by(state['grouping'], x, maintain_order=True)
        .agg(value=pl.sum('value'))
        .filter(pl.col.value > 0)
        .group_by(state['grouping'], maintain_order=True)
        .agg(
            new_x_start=pl.min(x).replace(new_time_index, return_dtype=pl.Int64)
        )
    )

    output = (
        df.join(group_starts, on=state['grouping'])
        .with_columns(
            age=pl.col(x).replace(new_time_index, return_dtype=pl.Int64)
            - pl.col.new_x_start
        )
        .filter(pl.col.age >= 0)
    ).drop('new_x_start')

    return output


def _filter_by_time_range(
    df: pl.DataFrame, state: dict[str, typing.Any]
) -> pl.DataFrame:
    import polars as pl
    import tooltime

    if state['time_window'] != 'all':
        if state['xalign'] == 'age':
            x = state['sample_interval']
            if x == 'date':
                age_unit = 86400
            elif x == 'week':
                age_unit = 7 * 86400
            elif x == 'month':
                age_unit = 30 * 86400
            else:
                raise Exception(
                    'invalid sample_interval: ' + str(state['sample_interval'])
                )
            max_age = (
                tooltime.timelength_to_seconds(state['time_window']) / age_unit
            )
            max_age = max(max_age, 1)
            df = df.filter(pl.col.age <= max_age)
        else:
            start_time = tooltime.timestamp_to_seconds(
                state['now']
            ) - tooltime.timelength_to_seconds(state['time_window'])
            df = df.filter((pl.col.timestamp >= start_time * 1e3))
    return df


def _add_total_entry(
    df: pl.DataFrame, state: dict[str, typing.Any]
) -> pl.DataFrame:
    import polars as pl

    if state['format'] == 'line' and state['xalign'] == 'age':
        x_dimension = 'age'
    else:
        x_dimension = 'timestamp'
    new_columns: dict[str, str | pl.Expr] = {
        state['grouping']: pl.lit('TOTAL').alias(state['grouping']),
        'interval': 'interval',
        'timestamp': 'timestamp',
        x_dimension: x_dimension,
        'value': 'value',
    }
    unused_columns = [
        column for column in df.columns if column not in new_columns
    ]
    if len(unused_columns) > 0:
        df = df.drop(unused_columns)
    df_total = (
        df.group_by(x_dimension, maintain_order=True)
        .agg(
            pl.sum('value'),
            pl.first('interval'),
            # pl.first('timestamp'),
        )
        .select(*[new_columns[key] for key in df.columns])
    )
    df = pl.concat([df, df_total])

    return df


def _convert_to_relative(
    df: pl.DataFrame, state: dict[str, typing.Any]
) -> pl.DataFrame:
    import polars as pl

    initial_value_per_group = df.group_by(
        state['grouping'], maintain_order=True
    ).agg(initial_value=pl.first('value'))
    df = df.filter(pl.col.value.is_not_null() & (pl.col.value > 0))
    df = df.join(initial_value_per_group, on=state['grouping'], how='left')
    df = df.filter(pl.col.initial_value >= 0.00001)
    df = (
        df.with_columns(value=pl.col.value / pl.col.initial_value)
        .with_columns(value=pl.col.value.replace({float('inf'): 0}))
        .fill_nan(None)
        .fill_null(0)
        .drop('initial_value')
    )
    return df


def _convert_to_percent(
    df: pl.DataFrame, state: dict[str, typing.Any]
) -> pl.DataFrame:
    import polars as pl

    if state['format'] == 'line' and state['xalign'] == 'age':
        x_dimension = 'age'
    else:
        x_dimension = 'timestamp'
    df = df.with_columns(value=pl.col.value / pl.sum('value').over(x_dimension))
    return df


def _sort_data(df: pl.DataFrame, state: dict[str, typing.Any]) -> pl.DataFrame:
    import polars as pl

    ranks = (
        df.group_by(state['grouping'])
        .agg(pl.sum('value'))
        .sort('value', descending=True)
        .with_row_index()
        .rename({'index': 'rank'})
    )
    return (
        df.join(
            ranks[[state['grouping'], 'rank']],
            on=state['grouping'],
            how='left',
        )
        .sort('timestamp', 'rank')
        .drop('rank')
    )
