from __future__ import annotations

import typing

from mince import transforms
from ... import raw_figures
from . import timeseries_data
from . import timeseries_styles

if typing.TYPE_CHECKING:
    import polars as pl
    import plotly.graph_objects as go  # type: ignore
    from mince import types


def create_time_series_fig(
    df: pl.DataFrame,
    state: dict[str, typing.Any],
    debug: bool,
    ui_spec: types.UiSpec,
    title: str | None = None,
) -> go.Figure:
    import time

    data_date_range = transforms.get_date_range(df)

    # prepare data
    start_time = time.time()
    df = timeseries_data._prepare_time_series_data(df, state, ui_spec=ui_spec)
    end_time = time.time()

    # create style kwargs
    style_kwargs = timeseries_styles._get_timeseries_style_kwargs(
        state, df, data_date_range=data_date_range, ui_spec=ui_spec, title=title
    )

    # print debug messages
    if debug:
        print()
        print('filtered data')
        print(
            'data filtering took',
            '%.6f' % ((end_time - start_time) * 1000),
            'milliseconds',
        )
        print('columns:', df.columns)
        print(df)

    # plot
    if state['format'] in ['line', 'line %']:
        return raw_figures.plot_line(df, **style_kwargs)
    elif state['format'] in ['area', 'area %']:
        return raw_figures.plot_stacked_bar(df, **style_kwargs)
    else:
        raise Exception('invalid format: ' + str(state['format']))
