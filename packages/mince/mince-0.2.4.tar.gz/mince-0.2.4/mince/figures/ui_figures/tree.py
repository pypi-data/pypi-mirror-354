from __future__ import annotations

import typing

from mince import specs
from ... import dashboards
from .. import raw_figures

if typing.TYPE_CHECKING:
    import polars as pl
    import plotly.graph_objects as go  # type: ignore
    from mince import types


ui_interval_to_df_interval = {
    'date': 'day',
    'week': 'week',
    'month': 'month',
}


def create_treemap_fig(
    df: pl.DataFrame,
    state: dict[str, typing.Any],
    ui_spec: types.UiSpec,
    data_date_range: tuple[int, int],
    title: str | None = None,
) -> go.Figure:
    df = _prepare_treemap_data(df, state, ui_spec=ui_spec)
    styles = _get_treemap_styles(
        df, state, ui_spec, data_date_range, title=title
    )
    return raw_figures.create_treemap(df=df, **styles)


def _prepare_treemap_data(
    df: pl.DataFrame, state: dict[str, typing.Any], ui_spec: types.UiSpec
) -> pl.DataFrame:
    import polars as pl
    import tooltime

    # filter by metric
    metric = dashboards.get_df_metric(state, ui_spec)
    df = df.filter(pl.col.metric == metric)

    metric_type = ui_spec['metrics'][metric]['type']

    if metric_type == 'point_in_time':
        now = tooltime.timestamp_to_seconds(state['now']) * 1e3
        df = df.filter(pl.col.timestamp == now)

    elif metric_type == 'unique':
        # filter sample_interval
        ui_interval = state['sample_interval']
        interval = ui_interval_to_df_interval[ui_interval]
        df = df.filter(pl.col.interval == interval)

        # select the closest point to now
        time_values = df['timestamp'].sort().unique()
        now = tooltime.timestamp_to_seconds(state['now']) * 1e3
        time_index = time_values.cast(pl.Int64).search_sorted(now)
        if time_index == len(time_values):
            time_index = -1
        time = time_values[time_index]
        df = df.filter(pl.col.timestamp == time)

    elif metric_type in ['sum', 'min', 'max']:
        df = df.filter(pl.col.interval == 'day')

        # filter time window
        end_time = tooltime.timestamp_to_seconds(state['now'])
        if state['time_window'] == 'all':
            df = df.filter(pl.col.timestamp <= end_time * 1e3)
        else:
            window = tooltime.timelength_to_seconds(state['time_window'])
            start_time = end_time - window
            df = df.filter(
                pl.col.timestamp > start_time * 1e3,
                pl.col.timestamp <= end_time * 1e3,
            )

        if metric_type == 'sum':
            agg_function = pl.sum('value')
        elif metric_type == 'min':
            agg_function = pl.min('value')
        elif metric_type == 'max':
            agg_function = pl.max('value')
        else:
            raise Exception()

        # aggregate
        df = (
            df.filter(pl.col.metric == metric)
            .group_by(*ui_spec['schema']['group_columns'])
            .agg(
                agg_function,
                min_timestamp=pl.min('timestamp'),
                max_timestamp=pl.max('timestamp'),
            )
        )
    else:
        raise Exception('invalid metric_type for treemap')

    return df


def _get_treemap_styles(
    df: pl.DataFrame,
    state: dict[str, typing.Any],
    ui_spec: types.UiSpec,
    data_date_range: tuple[int, int],
    title: str | None = None,
) -> dict[str, typing.Any]:
    # create title
    if title is None:
        title = _create_tree_title(
            df=df,
            state=state,
            data_date_range=data_date_range,
            ui_spec=ui_spec,
        )

    # get prefix
    metric = dashboards.get_df_metric(state, ui_spec=ui_spec)
    metric_spec = ui_spec['metrics'][metric]
    if metric_spec['unit'] == '$':
        prefix = '$'
    else:
        prefix = None

    if len(ui_spec['groupings']) == 1:
        subgrouping = None
    elif len(ui_spec['groupings']) == 2:
        if state['grouping'] == ui_spec['groupings'][0]:
            subgrouping = ui_spec['groupings'][1]
        else:
            subgrouping = ui_spec['groupings'][0]
    elif len(ui_spec['groupings']) > 2:
        raise NotImplementedError('multiple subgroupings')
    else:
        raise Exception('no groupings specified')

    return {
        'title': title,
        'grouping': state['grouping'],
        'subgrouping': subgrouping,
        'metric': metric,
        'prefix': prefix,
        'colors': ui_spec.get('colors'),
    }


def _create_tree_title(
    df: pl.DataFrame,
    state: dict[str, typing.Any],
    data_date_range: tuple[int, int],
    ui_spec: types.UiSpec,
) -> str:
    import tooltime

    metric = dashboards.get_df_metric(state, ui_spec=ui_spec)
    metric_spec = ui_spec['metrics'][metric]

    title_prefix = ui_spec['title_prefix']
    title_infix = ui_spec['title_infix']
    title_postfix = ui_spec['title_postfix']

    if state['metric'] in ui_spec['submetrics']:
        submetric = specs.state_to_alias(
            state['submetric'], 'submetric', ui_spec
        ).lower()
        metric_str: str = submetric
    else:
        metric_str = specs.state_to_alias(
            state['metric'], 'metric', ui_spec
        ).lower()
    metric_str = metric_str.title()

    if title_infix is not None:
        metric_str = title_infix + ' ' + metric_str
    if title_postfix is not None:
        metric_str = metric_str + ' ' + title_postfix

    if metric_spec['type'] in ['sum', 'min', 'max']:
        title = metric_str
        min_date = tooltime.timestamp_to_date(df['min_timestamp'].min())  # type: ignore
        max_date = tooltime.timestamp_to_date(df['max_timestamp'].max())  # type: ignore
        title += ' over ' + '[' + min_date + ', ' + max_date + ']'
    elif metric_spec['type'] == 'unique':
        title = metric_str + ' during '
        dt = tooltime.timestamp_to_date(df['timestamp'].max())  # type: ignore
        if state['sample_interval'] == 'date':
            dt_str = 'day of ' + dt
        elif state['sample_interval'] == 'week':
            dt_str = 'week of ' + dt
        elif state['sample_interval'] == 'month':
            dt_str = 'month of ' + dt[:7]
        else:
            raise Exception(
                'invalid sampling_interval ' + str(state['sample_interval'])
            )
        title += dt_str
    else:
        title = metric_str
        title += ' ' + tooltime.timestamp_to_date(df['timestamp'].max())  # type: ignore

    if title_prefix is not None:
        title = title_prefix + title

    return title
