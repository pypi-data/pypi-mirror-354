from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mince import types
    import polars as pl


def get_series_columns(schema: dict[str, types.ColumnType]) -> list[str]:
    return [
        column
        for column in schema.keys()
        if column not in ['timestamp', 'value']
    ]


def get_default_columns() -> dict[str, types.ColumnType]:
    import polars as pl

    return {
        'metric': pl.String,
        'timestamp': pl.Datetime(time_unit='ms'),
        'interval': pl.String,  # point, day, week, month
        'value': pl.Float64,
        'complete': pl.Boolean,
    }


def get_blank_dataframe(ui_spec: types.UiSpec) -> pl.DataFrame:
    """get black dataframe conforming to data schema"""
    import polars as pl

    return pl.DataFrame([], schema=ui_spec['schema']['columns'])
