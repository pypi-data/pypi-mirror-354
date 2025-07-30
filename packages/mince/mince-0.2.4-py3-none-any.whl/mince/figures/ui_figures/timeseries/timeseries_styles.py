from __future__ import annotations

from typing import Any, TYPE_CHECKING

from mince import dashboards
from mince import specs

if TYPE_CHECKING:
    import polars as pl
    from mince import types


def _get_timeseries_style_kwargs(
    state: dict[str, Any],
    df: pl.DataFrame,
    data_date_range: tuple[int, int],
    ui_spec: types.UiSpec,
    title: str | None = None,
) -> dict[str, Any]:
    # get yscale
    log_y = False
    if state['format'] == 'line' and state['yscale'] == 'log':
        log_y = True

    relative_y = False
    if state['format'] == 'line' and state['yscale'] == 'relative':
        relative_y = True

    # get ytick format
    df_metric = dashboards.get_df_metric(state=state, ui_spec=ui_spec)
    metric_spec = ui_spec['metrics'][df_metric]
    if state['format'] in ['line %', 'area %']:
        ytick_format = '%'
    elif metric_spec['unit'] in ['usd', 'USD', '$']:
        ytick_format = '$'
    elif metric_spec['unit'] == 'bytes':
        ytick_format = 'bytes'
    else:
        ytick_format = None

    # get title
    if title is None:
        title = _create_timeseries_title(
            df=df, state=state, data_date_range=data_date_range, ui_spec=ui_spec
        )

    # get ylabel
    ylabel = title.lower()
    if state['format'] in ['line %', 'area %']:
        ylabel = ylabel + ' share'

    # get xlabel
    if state['sample_interval'] == 'month':
        xlabel = 'month'
    elif state['sample_interval'] == 'week':
        xlabel = 'week'
    elif state['sample_interval'] == 'date':
        xlabel = 'date'
    else:
        raise Exception(
            'invalid selected sample_interval: ' + str(state['sample_interval'])
        )

    x = 'timestamp'
    total = False
    hover = True

    colors = ui_spec.get('colors')

    if state['format'] == 'line':
        # toggle total entry
        if state['total'] == 'total':
            total = True
        elif state['total'] == 'no total':
            total = False
        else:
            raise Exception('unknown value for total: ' + str(state['total']))

        # toggle hover
        if state['hover'] == 'hover':
            hover = True
        elif state['hover'] == 'no hover':
            hover = False
        else:
            raise Exception('unknown value for hover: ' + str(state['hover']))

        # age-specific styles
        if state['xalign'] == 'age':
            if state['sample_interval'] == 'date':
                xlabel = 'days'
            else:
                xlabel = xlabel + 's'
            xlabel = state['grouping'] + ' age (' + xlabel + ')'
            x = 'age'

        # relative styles
        if state['ynormalize'] == 'relative':
            ytick_format = '%'

    # return options based on figure type
    df_metric = dashboards.get_df_metric(state, ui_spec)
    if state['format'] in ['line', 'line %']:
        return dict(
            metric=df_metric,
            grouping=state['grouping'],
            x=x,
            log_y=log_y,
            relative_y=relative_y,
            xlabel=xlabel,
            ylabel=ylabel,
            ytick_format=ytick_format,
            title=title,
            hover=hover,
            total=total,
            colors=colors,
        )
    elif state['format'] in ['area', 'area %']:
        styles: dict[str, Any] = dict(
            # metric=state['metric'],
            metric=df_metric,
            grouping=state['grouping'],
            x=x,
            xlabel=xlabel,
            ylabel=ylabel,
            ytick_format=ytick_format,
            title=title,
            colors=colors,
            interval=state['sample_interval'],
        )
        if state['format'] == 'area %':
            styles['ylim'] = [0, 1]
        return styles
    else:
        raise Exception('invalid format')


def _create_timeseries_title(
    df: pl.DataFrame,
    state: dict[str, Any],
    data_date_range: tuple[int, int],
    ui_spec: types.UiSpec,
) -> str:
    df_metric = dashboards.get_df_metric(state, ui_spec)
    if df_metric in ui_spec['submetrics']:
        submetric = specs.state_to_alias(
            state['submetric'], 'submetric', ui_spec
        ).lower()
        title: str = submetric
    else:
        title = specs.state_to_alias(df_metric, 'metric', ui_spec).lower()

    title_prefix = ui_spec['title_prefix']
    title_infix = ui_spec['title_infix']
    title_postfix = ui_spec['title_postfix']

    if title_infix is not None:
        title = title_infix + ' ' + title
    if title_postfix is not None:
        title = title + ' ' + title_postfix

    if (
        state['cumulative'] in ['cumulative (window)', 'cumulative (t=0)']
        and ui_spec['metrics'][df_metric]['type'] == 'sum'
    ):
        title = 'Cumulative ' + title
    else:
        title = (
            specs.state_to_alias(
                state['sample_interval'], 'sample_interval', ui_spec
            ).title()
            + ' '
            + title
        )

    if title_prefix is not None:
        title = title_prefix + title

    if (
        state['cumulative'] in ['cumulative (window)', 'cumulative (t=0)']
        and ui_spec['metrics'][df_metric]['type'] == 'sum'
    ):
        import tooltime

        if state['cumulative'] == 'cumulative (t=0)':
            start_date = tooltime.timestamp_to_date(data_date_range[0])
        elif state['cumulative'] == 'cumulative (window)':
            start_date = tooltime.timestamp_to_date(df['timestamp'].min())  # type: ignore
        else:
            raise Exception()
        end_date = tooltime.timestamp_to_date(df['timestamp'].max())  # type: ignore
        title += ' from ' + start_date + ' to ' + end_date

    return title.title()
