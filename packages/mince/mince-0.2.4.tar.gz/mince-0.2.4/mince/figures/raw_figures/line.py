from __future__ import annotations

import typing

if typing.TYPE_CHECKING:
    import polars as pl
    import plotly.graph_objects as go  # type: ignore


def plot_line(
    df: pl.DataFrame,
    metric: str,
    grouping: str,
    x: str = 'x',
    log_y: bool = False,
    relative_y: bool = False,
    xlabel: str | None = None,
    ylabel: str | None = None,
    ytick_format: typing.Literal['$', '%', 'bytes'] | None = None,
    title: str | None = None,
    hover: bool = True,
    total: bool = False,
    colors: typing.Mapping[str, str] | None = None,
) -> go.Figure:
    import plotly.express as px  # type: ignore
    import polars as pl
    import toolstr

    # create formatted values
    if ytick_format == '$':
        toolstr_kwargs: typing.Mapping[str, typing.Any] = {
            'order_of_magnitude': True,
            'decimals': 1,
            'prefix': '$',
        }
    elif ytick_format == '%':
        toolstr_kwargs = {'percentage': True, 'decimals': 1}
    elif ytick_format == 'bytes':
        max_value: float = df['value'].max()  # type: ignore
        if max_value < 1024:
            unit = 1
            unit_label = 'Bytes'
        elif max_value < 1024**2:
            unit = 1024
            unit_label = 'KB'
        elif max_value < 1024**3:
            unit = 1024**2
            unit_label = 'MB'
        elif max_value < 1024**4:
            unit = 1024**3
            unit_label = 'GB'
        else:
            unit = 1024**4
            unit_label = 'TB'
        toolstr_kwargs = {'postfix': ' ' + unit_label, 'decimals': 2}
        if ylabel is None:
            ylabel = ''
        ylabel = ylabel + ' (' + unit_label + ')'
        df = df.with_columns(pl.col.value / unit)
    else:
        toolstr_kwargs = {'order_of_magnitude': True, 'decimals': 1}
    df = df.with_columns(
        formatted_value=pl.col.value.map_elements(
            lambda x: toolstr.format(x, **toolstr_kwargs),
            return_dtype=pl.String,
        )
    )

    fig = px.line(
        df,
        x=x,
        y='value',
        color=grouping,
        color_discrete_map=colors,
        custom_data=['formatted_value'],
    )
    fig.update_traces(line=dict(width=3))

    if total:
        fig.update_traces(
            line=dict(width=5),
            selector=dict(name='TOTAL'),
        )

    label_font = {
        'size': 18,
        'color': 'black',
        'family': 'monospace',
    }
    if title is None:
        title = metric
    title_kwargs = {
        'text': title,
        'y': 0.99,
        'font': {'size': 28, 'color': 'black', 'family': 'monospace'},
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top',
    }
    axis = {
        'showgrid': True,
        'gridcolor': '#DFDFDF',
        'gridwidth': 1,
        'griddash': 'dot',
    }
    if ylabel is None:
        ylabel = metric
    fig.update_layout(
        hoverlabel={
            'font_size': 12,
        },
    )
    fig.update_layout(
        paper_bgcolor='white',
        plot_bgcolor='white',
        dragmode='zoom',
        xaxis=dict(axis, title=xlabel),
        yaxis=dict(axis, title=ylabel),
        bargap=0,
        bargroupgap=0,
        xaxis_fixedrange=True,
        xaxis_type='category',
        yaxis_fixedrange=True,
        legend_title=None,
        legend_font={'size': 18, 'color': 'black', 'family': 'monospace'},
        # legend_traceorder='reversed',
        title=title_kwargs,
        hovermode='x unified',
    )
    if log_y:
        fig.update_layout(yaxis_type='log')
    fig.update_traces(
        marker_line_width=0.1,
        marker_line_color='black',
        hoverinfo='text+x+y',
    )

    label_font = {
        'size': 18,
        'color': 'black',
        'family': 'monospace',
    }

    if df[x].dtype == pl.Datetime:
        fig.update_xaxes(
            nticks=7,
            # autotickangles=[90],
        )
        fig.update_layout(
            xaxis=dict(
                tickformat='%Y-%m-%d',
                type='date',
            ),
        )
    fig.update_xaxes(
        title_font=label_font,
        tickfont=label_font,
        showspikes=True,
        spikesnap='cursor',
        spikemode='across',
        spikethickness=1,
        spikecolor='black',
        spikedash='solid',
    )
    fig.update_yaxes(
        title_font=label_font,
        tickfont=label_font,
        showspikes=True,
        spikesnap='cursor',
        spikemode='across',
        spikethickness=1,
        spikecolor='black',
        spikedash='solid',
    )

    if hover:
        fig.update_traces(
            hovertemplate='%{fullData.name} %{customdata[0]}<extra></extra>'
        )
    else:
        fig.update_traces(hovertemplate=None)
        fig.update_traces(hoverinfo='none')

    # set ytick format
    if ytick_format is not None:
        if ytick_format == '$':
            fig.update_yaxes(tickprefix='$')
        elif ytick_format == '%':
            fig.update_yaxes(tickformat='.0%')
        elif ytick_format == 'bytes':
            pass
        else:
            raise Exception('invalid yformat: ' + str(ytick_format))

    return fig
