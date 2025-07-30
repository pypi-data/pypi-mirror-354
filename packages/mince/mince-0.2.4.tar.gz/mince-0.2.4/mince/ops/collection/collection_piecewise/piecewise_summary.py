from __future__ import annotations

import typing

import mince

if typing.TYPE_CHECKING:
    from . import piecewise_collector


def print_summary(
    output: piecewise_collector.Output,
    verbose: int,
    max_concurrent_queries: int,
) -> None:
    if verbose >= 2:
        import toolstr

        print()
        toolstr.print_header('Skipping chunks')
        if len(output['skip_slugs']) == 0:
            print('[none]')
        for slug in output['skip_slugs']:
            print(slug)
        print()
        toolstr.print_header('Running chunks')
        if len(output['run_slugs']) == 0:
            print('[none]')
        for slug in output['run_slugs']:
            print(slug)

    if verbose >= 1:
        n_run = len(output['coroutines'])
        n_skip = len(output['skip_slugs'])
        n_concurrent = min(n_run, max_concurrent_queries)
        print(
            '\n\nrunning',
            n_run,
            'collection chunks,',
            n_concurrent,
            'chunks at a time',
            '(skipping',
            n_skip,
            'existing chunks)',
            '\n',
        )


def get_chunk_slug(
    start_time: int | float,
    end_time: int | float,
    tags: dict[str, str],
    interval: mince.Interval,
    data_dir: str | None = None,
    path_template: str | None = None,
    verbose: int = 1,
    skip_incomplete_intervals: bool = False,
) -> str:
    import tooltime

    start_str = tooltime.timestamp_to_date(start_time)
    end_str = tooltime.timestamp_to_date(end_time)
    tag_str = [k + '=' + v for k, v in tags.items()]
    return ' '.join([start_str, end_str, 'interval=' + interval, *tag_str])
