from __future__ import annotations

import typing

import mince

if typing.TYPE_CHECKING:
    import polars as pl


def compute_time_chunks(
    start_time: float,
    end_time: float,
    chunk_size: str,
    interval: mince.Interval,
    tags: dict[str, str],
    get_chunk_time_range: typing.Callable[..., tuple[int, int]] | None,
    skip_incomplete_intervals: bool,
) -> pl.DataFrame:
    import tooltime

    # convert chunk_size to be integer multiple of interval
    interval_chunk_size = round_up_chunk_size(chunk_size, interval)

    # adjust target data range
    if get_chunk_time_range is None:
        use_start, use_end = start_time, end_time
    else:
        use_start, use_end = get_chunk_time_range(
            start_time=start_time,
            end_time=end_time,
            interval=interval,
            tags=tags,
        )

    return tooltime.get_intervals(
        start=use_start,
        end=use_end,
        interval=interval_chunk_size,
        include_incomplete=not skip_incomplete_intervals,
        clip_inward=True,
    )


def round_up_chunk_size(chunk_size: str, interval: mince.Interval) -> str:
    """round up chunk size so that it can be evenly divided by interval
    - each chunk must be an integer multiple of the sampling interval
    - chunks in a chunkset do not need to all be the same size
    """
    import math

    chunk_count = int(chunk_size[:-1])
    chunk_unit = chunk_size[-1]

    if interval == 'hour':  # type: ignore
        # all chunk units are evently divisible into hours
        return chunk_size
    elif interval == 'day':
        if chunk_unit == 'h':
            return str(math.ceil(chunk_count / 24)) + 'd'
        elif chunk_unit == 'd':
            return chunk_size
        elif chunk_unit == 'w':
            return chunk_size
        elif chunk_unit == 'M':
            return chunk_size
        elif chunk_unit == 'y':
            return chunk_size
        else:
            raise Exception('invalid chunk unit')
    elif interval == 'week':
        if chunk_unit == 'h':
            return str(math.ceil(chunk_count / 7 / 24)) + 'w'
        elif chunk_unit == 'd':
            return str(math.ceil(chunk_count / 7)) + 'w'
        elif chunk_unit == 'w':
            return chunk_size
        elif chunk_unit == 'M':
            return str(math.ceil(4.43 * chunk_count)) + 'w'
        elif chunk_unit == 'y':
            return str(math.ceil(52.3 * chunk_count)) + 'w'
        else:
            raise Exception('invalid chunk unit')
    elif interval == 'month':
        if chunk_unit == 'h':
            return str(math.ceil(chunk_count / 28 / 24)) + 'M'
        elif chunk_unit == 'd':
            return str(math.ceil(chunk_count / 28)) + 'M'
        elif chunk_unit == 'w':
            return str(math.ceil(chunk_count / 4)) + 'M'
        elif chunk_unit == 'M':
            return chunk_size
        elif chunk_unit == 'y':
            return chunk_size
        else:
            raise Exception('invalid chunk unit')
    elif interval == 'year':
        if chunk_unit == 'h':
            return str(math.ceil(chunk_count / 365 / 24)) + 'y'
        elif chunk_unit == 'd':
            return str(math.ceil(chunk_count / 365)) + 'y'
        elif chunk_unit == 'w':
            return str(math.ceil(chunk_count / 52)) + 'y'
        elif chunk_unit == 'M':
            return str(math.ceil(chunk_count / 12)) + 'y'
        elif chunk_unit == 'y':
            return chunk_size
        else:
            raise Exception('invalid chunk unit')
    else:
        raise Exception('invalid sampling interval: ' + str(interval))
