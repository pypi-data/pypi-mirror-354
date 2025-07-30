from __future__ import annotations

from typing import TYPE_CHECKING

from . import schema_structure

if TYPE_CHECKING:
    from mince import types


def partial_schema_to_whole(
    partial: types.DataSchemaPartial,
) -> types.DataSchema:
    import polars as pl

    raw_group_columns = partial.get('group_columns')
    if raw_group_columns is None:
        group_columns = []
    else:
        group_columns = raw_group_columns

    columns = {}
    raw_columns = partial.get('columns')
    if raw_columns is None:
        raise Exception('must specify columns')
    elif isinstance(raw_columns, list):
        default_columns = schema_structure.get_default_columns()
        for column in raw_columns:
            dtype = default_columns.get(column)
            if dtype is not None:
                columns[column] = dtype
            else:
                columns[column] = pl.String
    elif isinstance(raw_columns, dict):
        default_columns = schema_structure.get_default_columns()
        for column, dtype in raw_columns.items():
            if dtype is not None:
                columns[column] = dtype
            elif column in default_columns:
                columns[column] = default_columns[column]
            else:
                columns[column] = pl.String
    else:
        raise Exception('invalid column format')

    return {
        'columns': columns,
        'group_columns': group_columns,
    }
