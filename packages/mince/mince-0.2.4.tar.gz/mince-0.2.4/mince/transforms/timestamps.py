from __future__ import annotations

import typing

if typing.TYPE_CHECKING:
    import polars as pl
    import tooltime


def get_date_range(df: pl.DataFrame) -> tuple[int, int]:
    import datetime
    import tooltime

    if len(df) == 0:
        raise Exception('empty dataframe')

    start_time: datetime.datetime = df['timestamp'].min()  # type: ignore
    end_time: datetime.datetime = df['timestamp'].max()  # type: ignore

    return (
        tooltime.timestamp_to_seconds(start_time),
        tooltime.timestamp_to_seconds(end_time),
    )


def week_column(*, time_column: str | None = None) -> pl.Expr:
    if time_column is None:
        time_column = 'timestamp'
    return (
        pl.col(time_column)
        .dt.offset_by('1d')
        .dt.truncate('1w')
        .dt.offset_by('-1d')
        .alias('week')
    )


def end_timestamp_column(*, time_column: str | None = None) -> pl.Expr:
    if time_column is None:
        time_column = 'timestamp'
    return (
        pl.when(interval='year')
        .then(pl.col(time_column).dt.truncate('1y').dt.offset_by('1y'))
        .when(interval='month')
        .then(pl.col(time_column).dt.truncate('1mo').dt.offset_by('1mo'))
        .when(interval='week')
        .then(week_column().dt.offset_by('1d'))
        .when(interval='day')
        .then(pl.col(time_column).dt.truncate('1d').dt.offset_by('1d'))
        .when(interval='hour')
        .then(pl.col(time_column).dt.truncate('1d').dt.offset_by('1d'))
        .otherwise(None)
        .alias('end_timestamp')
    )


def interval_completed_column(
    cutoff: tooltime.Timestamp,
    *,
    time_column: str | None = None,
) -> pl.Expr:
    import tooltime

    dt_cutoff = tooltime.timestamp_to_datetime(cutoff)
    return dt_cutoff < end_timestamp_column(time_column=time_column)
