from __future__ import annotations

import mince

import typing

if typing.TYPE_CHECKING:
    import tooltime
    import polars as pl


def create_piece_path(
    data_dir: str,
    path_template: str,
    interval: str,
    tags: dict[str, str],
    timestamp: tooltime.Timestamp | None,
    complete: bool | str,
) -> str:
    import os
    import tooltime

    if isinstance(complete, bool):
        if complete:
            complete_str = 'complete'
        else:
            complete_str = 'incomplete'
    elif isinstance(complete, str):
        if complete not in ['complete', 'incomplete', '*']:
            raise Exception('invalid value for complete parameter')
        complete_str = complete

    if timestamp is not None and timestamp != '*':
        dt = tooltime.timestamp_to_datetime(timestamp)
        if interval in ['hour', 'minute', 'second']:
            timestamp = dt.strftime('%Y-%m-%d_%H-%M-%S')
        elif interval in ['day', 'week']:
            timestamp = dt.strftime('%Y-%m-%d')
        elif interval == 'month':
            timestamp = dt.strftime('%Y-%m')
        elif interval == 'year':
            timestamp = dt.strftime('%Y')
        else:
            raise Exception('invalid interval')
    path = path_template.format(
        interval=interval, timestamp=timestamp, complete=complete_str, **tags
    )
    return os.path.join(data_dir, 'pieces', path)


def pieces_already_exist(
    path_template: str,
    data_dir: str,
    interval: mince.Interval,
    tags: dict[str, str],
    skip_incomplete_intervals: bool,
    start_time: float,
    end_time: float,
    verbose: int,
) -> bool:
    import os
    import tooltime

    duration = {'day': '1d', 'week': '1w', 'month': '1M', 'year': '1y'}.get(
        interval, interval
    )
    chunks = tooltime.get_intervals(
        interval=duration,
        start=start_time,
        end=end_time,
        include_incomplete=not skip_incomplete_intervals,
    )

    all_exist = True
    for timestamp in chunks['start']:
        path = create_piece_path(
            path_template=path_template,
            data_dir=data_dir,
            interval=interval,
            tags=tags,
            timestamp=timestamp,
            complete=True,
        )
        exists = os.path.exists(path)
        if not exists:
            if verbose <= 2:
                return False
            else:
                all_exist = False

        # print summary
        if verbose >= 3:
            if exists:
                label = 'EXISTS'
            else:
                label = 'MISSING'
            print(label, os.path.relpath(path, data_dir))

    return all_exist


def write_piece_files(
    path_template: str,
    data_dir: str,
    df: pl.DataFrame,
    interval: mince.Interval,
    tags: dict[str, str],
) -> None:
    import datetime
    import os
    import shutil

    partitions = df.partition_by(('timestamp', 'complete'), as_dict=True)
    for (timestamp, complete), sub_df in partitions.items():
        path = create_piece_path(
            path_template=path_template,
            data_dir=data_dir,
            interval=interval,
            tags=tags,
            timestamp=typing.cast(datetime.datetime, timestamp),
            complete=typing.cast(bool, complete),
        )
        os.makedirs(os.path.dirname(path), exist_ok=True)
        path_tmp = path + '_tmp'
        sub_df.write_parquet(path_tmp)
        shutil.move(path_tmp, path)

        # delete incomplete version
        if complete:
            incomplete_path = create_piece_path(
                path_template=path_template,
                data_dir=data_dir,
                interval=interval,
                tags=tags,
                timestamp=typing.cast(datetime.datetime, timestamp),
                complete=False,
            )
            if os.path.exists(incomplete_path):
                os.remove(incomplete_path)


def read_piece_files(
    data_dir: str,
    path_template: str,
    tag_names: typing.Sequence[str],
) -> dict[str, pl.DataFrame]:
    import polars as pl

    path = create_piece_path(
        data_dir=data_dir,
        path_template=path_template,
        interval='*',
        tags={tag_name: '*' for tag_name in tag_names},
        timestamp='*',
        complete='*',
    )

    return {'data': pl.read_parquet(path)}
