from __future__ import annotations

import typing

if typing.TYPE_CHECKING:
    import datetime
    import polars as pl

    class _PlotKwargs(typing.TypedDict, total=False):
        changes: pl.DataFrame
        interval: str
        metric: str
        group_by: list[str]
        min_relative_change: float | None
        min_abs_change: float | None
        metric_format: dict[str, typing.Any] | None


def compute_changes(
    df: pl.DataFrame,
    *,
    group_by: str | list[str],
    metric: str,
    intervals: list[str] | dict[str, pl.Expr] | None = None,
    now: datetime.datetime | None = None,
    timestamp_column: str = 'timestamp',
    allow_null_rows: bool = False,
    pre_aggregate: str | None = 'sum',
) -> pl.DataFrame:
    import polars as pl
    import datetime

    if pre_aggregate is not None:
        if isinstance(group_by, str):
            group_by = [group_by]
        if pre_aggregate == 'sum':
            df = df.group_by(timestamp_column, *group_by).agg(pl.sum(metric))
        else:
            raise Exception('invalid pre aggregation: ' + str(pre_aggregate))

    # determine now
    if now is None:
        now = (
            df[[timestamp_column, metric]]  # type: ignore
            .filter(pl.col(metric).is_not_null())[timestamp_column]
            .max()
        )
    if isinstance(now, datetime.date):
        now = datetime.datetime(now.year, now.month, now.day)
    if not isinstance(now, datetime.datetime):
        raise Exception('could not determine timestamp')

    # gather intervals
    if intervals is None:
        intervals = ['7d', '1mo', '1q', '1y']
    intervals = {
        interval: pl.lit(now).dt.offset_by('-' + interval)
        for interval in intervals
    }

    # build columns
    value_columns = {
        'value_' + interval: pl.col(metric)
        .filter(pl.col(timestamp_column) == timestamp)
        .last()
        for interval, timestamp in intervals.items()
    }
    abs_delta_columns = {
        'abs_delta_' + interval: pl.col.value_now - pl.col('value_' + interval)
        for interval in intervals.keys()
    }
    rel_delta_columns = {
        'rel_delta_' + interval: (
            pl.col.value_now - pl.col('value_' + interval)
        )
        / pl.col('value_' + interval)
        for interval in intervals.keys()
    }

    # compute changes
    changes = (
        df.group_by(group_by)
        .agg(
            value_now=pl.col(metric)
            .filter(pl.col(timestamp_column) == now)
            .last(),
            **value_columns,
        )
        .with_columns(
            **abs_delta_columns,
            **rel_delta_columns,
            t_now=pl.lit(now),
            **{'t_' + k: v for k, v in intervals.items()},
        )
    )

    # check for nulls
    if (
        not allow_null_rows
        and not changes.filter(pl.col.value_now.is_null()).is_empty()
    ):
        raise Exception(
            'some rows have missing values for timestamp, use allow_null_rows=True'
        )

    return changes


def summarize_changes(
    changes: pl.DataFrame,
    metric: str,
    interval: str,
    *,
    n: int = 10,
    metric_format: dict[str, typing.Any] | None = None,
    min_new_value: float | str | None = None,
    min_old_value: float | str | None = None,
) -> None:
    import polars as pl
    import toolstr

    if metric_format is None:
        metric_format = {}

    # filter data
    abs_column = 'abs_delta_' + interval
    rel_column = 'rel_delta_' + interval
    changes = changes.filter(
        pl.col(rel_column).is_not_null(), pl.col(rel_column).is_not_nan()
    )

    # new_value = 'value'
    t_start = changes['t_' + interval].last()
    t_now = changes['t_now'].last()
    new_value = 'value on\n' + str(t_now)[:10]
    display_abs = 'Δ ' + interval
    display_rel = '%Δ ' + interval
    old_value = 'value on\n' + str(t_start)[:10]

    # create table subsets
    group_by = changes.columns[: changes.columns.index('value_now')]
    selection = {
        old_value: 'value_' + interval,
        new_value: 'value_now',
        display_abs: abs_column,
        display_rel: rel_column,
    }
    display_changes = changes.select(*group_by, **selection)
    gainers = display_changes.filter(pl.col(display_abs) > 0)
    losers = display_changes.filter(pl.col(display_abs) < 0)
    abs_gainers = gainers.sort(display_abs, descending=True, nulls_last=True)
    abs_losers = losers.sort(display_abs, nulls_last=True)
    rel_gainers = gainers.sort(display_rel, descending=True, nulls_last=True)
    rel_losers = losers.sort(display_rel, nulls_last=True)
    if min_old_value is not None:
        rel_losers = rel_losers.filter(pl.col(new_value) >= min_old_value)
        abs_losers = abs_losers.filter(pl.col(new_value) >= min_old_value)
    if min_new_value is not None:
        rel_gainers = rel_gainers.filter(pl.col(new_value) >= min_new_value)
        abs_gainers = abs_gainers.filter(pl.col(new_value) >= min_new_value)

    # table formatting
    standard_format = {'order_of_magnitude': True, 'decimals': 1}
    column_formats: dict[str, dict[str, typing.Any]] = {
        new_value: standard_format,
        old_value: standard_format,
        display_abs: dict(standard_format, signed=True),
        display_rel: {'percentage': True, 'decimals': 1, 'signed': True},
    }
    column_formats[new_value].update(metric_format)
    column_formats[display_abs].update(metric_format)
    table_kwargs = {'column_formats': column_formats, 'indent': 4, 'compact': 4}

    # print preamble
    time_range = '(' + str(t_start)[:10] + ' to ' + str(t_now)[:10] + ')'
    toolstr.print_text_box(
        'Biggest movers for ' + metric + ', last ' + interval
    )

    # print largest gainers and losers
    print()
    toolstr.print_header(
        'Largest absolute gainers for `' + metric + '` ' + time_range
    )
    print('- n_entries:', toolstr.format(len(abs_gainers)))
    if min_new_value is not None:
        print('- filter: new_value > ', toolstr.format(min_new_value))
    print()
    toolstr.print_dataframe_as_table(abs_gainers[:n], **table_kwargs)  # type: ignore
    print()
    toolstr.print()
    print()
    toolstr.print_header('Largest relative gainers ' + time_range)
    print('- n_entries:', toolstr.format(len(rel_gainers)))
    if min_new_value is not None:
        print('- filter: new_value > ', toolstr.format(min_new_value))
    print()
    toolstr.print_dataframe_as_table(rel_gainers[:n], **table_kwargs)  # type: ignore
    print()
    toolstr.print()
    print()
    toolstr.print_header('Largest absolute losers ' + time_range)
    print('- n_entries:', toolstr.format(len(abs_losers)))
    if min_old_value is not None:
        print('- filter: old_value > ', toolstr.format(min_old_value))
    print()
    toolstr.print_dataframe_as_table(abs_losers[:n], **table_kwargs)  # type: ignore
    print()
    toolstr.print()
    print()
    toolstr.print_header('Largest relative losers ' + time_range)
    print('- n_entries:', toolstr.format(len(rel_losers)))
    if min_old_value is not None:
        print('- filter: old_value > ', toolstr.format(min_old_value))
    print()
    toolstr.print_dataframe_as_table(rel_losers[:n], **table_kwargs)  # type: ignore

    # print entries
    print()
    toolstr.print()
    print()
    entries = changes.sort('value_now', descending=True, nulls_last=True)
    entries = entries.select(*group_by, **selection)
    toolstr.print_header('Largest current entries')
    print('- n_entries:', toolstr.format(len(entries)))
    toolstr.print_dataframe_as_table(entries[:n], **table_kwargs)  # type: ignore


def _get_intervals(changes: pl.DataFrame) -> list[str]:
    return [
        column.split('abs_delta_')[1]
        for column in changes.columns
        if column.startswith('abs_delta_')
    ]


def _get_group_by(changes: pl.DataFrame) -> list[str]:
    return changes.columns[: changes.columns.index('value_now')]


def plot_changes_vs_size(
    changes: pl.DataFrame,
    metric: str,
    *,
    intervals: list[str] | None = None,
    group_by: list[str] | None = None,
    plot_kwargs: _PlotKwargs | None = None,
    min_relative_change: float | None = None,
    min_abs_change: float | None = None,
    metric_format: dict[str, typing.Any] | None = None,
) -> None:
    import toolplot

    toolplot.setup_plot_formatting()

    if intervals is None:
        intervals = _get_intervals(changes)
    if group_by is None:
        group_by = _get_group_by(changes)
    kwargs: _PlotKwargs = dict(
        changes=changes,
        group_by=group_by,
        metric=metric,
        min_relative_change=min_relative_change,
        min_abs_change=min_abs_change,
        metric_format=metric_format,
    )
    if plot_kwargs is not None:
        kwargs.update(plot_kwargs)
    for interval in intervals:
        kwargs['interval'] = interval
        _plot_changes(positive=True, change_type='relative', **kwargs)
        _plot_changes(positive=False, change_type='relative', **kwargs)
        _plot_changes(positive=True, change_type='absolute', **kwargs)
        _plot_changes(positive=False, change_type='absolute', **kwargs)


def _plot_changes(
    changes: pl.DataFrame,
    interval: str,
    metric: str,
    group_by: list[str],
    change_type: typing.Literal['absolute', 'relative'],
    positive: bool = True,
    min_relative_change: float | None = None,
    min_abs_change: float | None = None,
    metric_format: dict[str, typing.Any] | None = None,
) -> None:
    import polars as pl
    import matplotlib.pyplot as plt
    import toolplot

    # select subset of data
    if min_abs_change is None:
        min_abs_change = 0
    if min_relative_change is None:
        min_relative_change = 0.01
    if positive:
        data = changes.filter(
            pl.col('abs_delta_' + interval) > min_abs_change,
            pl.col.value_now > 0,
        )
        if change_type == 'relative':
            data = data.filter(
                pl.col('rel_delta_' + interval) > min_relative_change
            )
            yvals = data['rel_delta_' + interval]
        else:
            yvals = data['abs_delta_' + interval]
        xvals = data['value_now']
        color = 'green'
    else:
        data = changes.filter(
            pl.col('abs_delta_' + interval) < -min_abs_change,
            pl.col.value_now > 0,
        )
        if change_type == 'relative':
            data = data.filter(
                pl.col('rel_delta_' + interval) < -min_relative_change
            )
            yvals = -data['rel_delta_' + interval]
        else:
            yvals = -data['abs_delta_' + interval]
        xvals = data['value_' + interval]
        color = 'red'

    # skip if empty
    if len(data) == 0:
        print('no data, skipping plot')
        return

    # create scatterplot
    plt.plot(xvals, yvals, '.', color=color, markersize=10)
    name: list[str] | tuple[str] | None
    for name, x, y in zip(data[group_by].rows(), xvals, yvals):
        if name is None or name[0] is None:
            name = ['unlabeled'] * len(group_by)
        if x is not None and y is not None:
            plt.text(
                x,
                y,
                ' ' + '_'.join(name),
                fontsize=8,
            )
    plt.xscale('log')

    plt.yscale('log')
    if change_type == 'absolute' and min_abs_change > 0:
        ylim = plt.ylim()
        plt.ylim([max(ylim[0], min_abs_change), ylim[1]])

    if positive:
        plt.xlabel('\ncurrent value')
        if change_type == 'relative':
            toolplot.format_yticks(toolstr_kwargs={'percentage': True})
        else:
            ytick_format: dict[str, typing.Any] = {
                'order_of_magnitude': True,
                'decimals': 0,
            }
            if metric_format is not None:
                ytick_format.update(metric_format)
            toolplot.format_yticks(toolstr_kwargs=ytick_format)
    else:
        plt.xlabel('\nvalue ' + interval + ' ago')
        if change_type == 'relative':
            toolplot.format_yticks(
                toolstr_kwargs={'percentage': True, 'prefix': '–'}
            )
            plt.ylim([1, min_relative_change])
        else:
            ytick_format = {
                'order_of_magnitude': True,
                'decimals': 0,
                'prefix': '',
            }
            if metric_format is not None:
                ytick_format.update(metric_format)
            ytick_format['prefix'] = '−' + ytick_format['prefix']
            toolplot.format_yticks(toolstr_kwargs=ytick_format)
            ylim = plt.ylim()
            plt.ylim([ylim[1], ylim[0]])

    # label plot
    xtick_format = {'order_of_magnitude': True, 'decimals': 1}
    if metric_format is not None:
        xtick_format.update(metric_format)
    toolplot.format_xticks(
        toolstr_kwargs=xtick_format,
        rotation=0,
    )
    if change_type == 'relative':
        plt.ylabel('% change over ' + interval + '\n')
    else:
        plt.ylabel('abs change over ' + interval + '\n')
    toolplot.add_tick_grid()
    t_start = changes['t_' + interval].last()
    t_now = changes['t_now'].last()
    time_range = '(' + str(t_start)[:10] + ' to ' + str(t_now)[:10] + ')'
    plt.title(
        change_type.title()
        + ' changes in '
        + metric
        + ' for each '
        + '+'.join(group_by)
        + '\nduration = '
        + interval
        + ' '
        + time_range
    )
    plt.show()  # type: ignore
