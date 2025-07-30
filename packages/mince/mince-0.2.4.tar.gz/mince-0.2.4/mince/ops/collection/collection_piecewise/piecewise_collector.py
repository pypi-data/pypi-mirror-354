from __future__ import annotations

import typing

import mince

from . import piecewise_io
from .piecewise_io import pieces_already_exist
from . import piecewise_summary
from . import piecewise_times

if typing.TYPE_CHECKING:
    T = typing.TypeVar('T')
    import polars as pl

    class Chunk(typing.TypedDict):
        start_time: float
        end_time: float
        interval: mince.Interval
        skip_incomplete_intervals: bool
        data_dir: str
        path_template: str
        tags: dict[str, str]
        verbose: int

    class Output(typing.TypedDict):
        coroutines: list[typing.Coroutine[typing.Any, typing.Any, None]]
        run_slugs: list[str | None]
        skip_slugs: list[str | None]


async def async_collect_data_piecewise(
    data_dir: str,
    path_template: str,
    start_time: float,
    end_time: float,
    intervals: list[mince.Interval],
    skip_incomplete_intervals: bool,
    max_concurrent_queries: int,
    chunk_size: str,
    skip_existing_files: bool,
    async_collect_df: mince.AsyncDfCollector,
    tags: dict[str, list[str]],
    get_chunk_time_range: typing.Callable[..., tuple[int, int]] | None = None,
    verbose: int = 1,
    dry: bool = False,
) -> dict[str, pl.DataFrame]:
    # collect pieces
    await _async_collect_data_pieces(
        data_dir=data_dir,
        start_time=start_time,
        end_time=end_time,
        intervals=intervals,
        skip_incomplete_intervals=skip_incomplete_intervals,
        max_concurrent_queries=max_concurrent_queries,
        chunk_size=chunk_size,
        skip_existing_files=skip_existing_files,
        async_collect_df=async_collect_df,
        get_chunk_time_range=get_chunk_time_range,
        path_template=path_template,
        tags=tags,
        verbose=verbose,
        dry=dry,
    )

    if dry:
        return {}

    # load results
    return piecewise_io.read_piece_files(
        data_dir=data_dir,
        path_template=path_template,
        tag_names=list(tags.keys()),
    )


async def _async_collect_data_pieces(
    data_dir: str,
    start_time: float,
    end_time: float,
    intervals: list[mince.Interval],
    skip_incomplete_intervals: bool,
    max_concurrent_queries: int,
    chunk_size: str,
    skip_existing_files: bool,
    async_collect_df: mince.AsyncDfCollector,
    get_chunk_time_range: typing.Callable[..., tuple[int, int]] | None,
    path_template: str,
    tags: dict[str, list[str]],
    verbose: int,
    dry: bool,
) -> None:
    if verbose >= 3:
        print('\nFile existence checks\n' + '─' * 21)
    output: Output = {'coroutines': [], 'run_slugs': [], 'skip_slugs': []}
    for tag_combo in compute_tag_combos(tags):
        for interval in intervals:
            chunks = piecewise_times.compute_time_chunks(
                start_time=start_time,
                end_time=end_time,
                chunk_size=chunk_size,
                interval=interval,
                tags=tag_combo,
                get_chunk_time_range=get_chunk_time_range,
                skip_incomplete_intervals=False,
            )
            for chunk_start, chunk_end in chunks[['start', 'end']].rows():
                chunk: Chunk = {
                    'start_time': chunk_start,
                    'end_time': chunk_end,
                    'interval': interval,
                    'skip_incomplete_intervals': skip_incomplete_intervals,
                    'data_dir': data_dir,
                    'path_template': path_template,
                    'tags': tag_combo,
                    'verbose': verbose,
                }
                slug = None
                if verbose >= 2:
                    slug = piecewise_summary.get_chunk_slug(**chunk)
                if skip_existing_files and pieces_already_exist(**chunk):
                    output['skip_slugs'].append(slug)
                    continue
                output['run_slugs'].append(slug)
                coroutine = _async_collect_piece_chunk(
                    dry=dry, async_collect_df=async_collect_df, **chunk
                )
                output['coroutines'].append(coroutine)

    piecewise_summary.print_summary(output, verbose, max_concurrent_queries)

    await semaphore_gather(max_concurrent_queries, *output['coroutines'])


async def _async_collect_piece_chunk(
    *,
    data_dir: str,
    path_template: str,
    interval: mince.Interval,
    skip_incomplete_intervals: bool,
    start_time: int | float,
    end_time: int | float,
    async_collect_df: mince.AsyncDfCollector,
    tags: dict[str, str],
    verbose: int,
    dry: bool,
) -> None:
    import polars as pl
    import tooltime

    # print summary
    if verbose >= 1:
        slug = piecewise_summary.get_chunk_slug(
            start_time=start_time,
            end_time=end_time,
            tags=tags,
            interval=interval,
        )
        print('doing', slug)

    if dry:
        return

    # get data
    df = await async_collect_df(
        interval=interval,
        start_time=tooltime.timestamp_to_seconds(start_time),
        end_time=tooltime.timestamp_to_seconds(end_time),
        tags=tags,
    )

    # add completeness information
    targets = tooltime.get_intervals(
        interval=interval,
        start=start_time,
        end=end_time,
        include_incomplete=not skip_incomplete_intervals,
    ).select(timestamp='start', complete=pl.col.completeness == 'complete')
    df = df.join(targets, on='timestamp', how='inner')
    if df['complete'].is_null().any():
        raise Exception('unexpected timestamps in collected data')

    # write pieces
    piecewise_io.write_piece_files(
        data_dir=data_dir,
        path_template=path_template,
        df=df,
        interval=interval,
        tags=tags,
    )


def compute_tag_combos(
    tags: dict[str, list[str]],
) -> typing.Generator[dict[str, str]]:
    import itertools

    for tag_combo_values in itertools.product(*tags.values()):
        yield dict(zip(tags.keys(), tag_combo_values))


async def semaphore_gather(
    n_concurrent: int, *tasks: typing.Awaitable[T]
) -> list[T]:
    import asyncio

    semaphore = asyncio.Semaphore(n_concurrent)

    async def semaphore_task(task: typing.Awaitable[T]) -> T:
        async with semaphore:
            return await task

    return await asyncio.gather(*(semaphore_task(task) for task in tasks))
