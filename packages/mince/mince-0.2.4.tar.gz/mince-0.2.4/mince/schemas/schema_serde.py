from __future__ import annotations

import typing

if typing.TYPE_CHECKING:
    import mince.types
    import polars as pl


def get_polars_type_map() -> dict[mince.types.ColumnType, str]:
    return {
        pl.Int8: 'Int8',
        pl.Int16: 'Int16',
        pl.Int32: 'Int32',
        pl.Int64: 'Int64',
        pl.UInt8: 'UInt8',
        pl.UInt16: 'UInt16',
        pl.UInt32: 'UInt32',
        pl.UInt64: 'UInt64',
        pl.Float32: 'Float32',
        pl.Float64: 'Float64',
        pl.Decimal: 'Decimal',
        pl.Boolean: 'Boolean',
        pl.Binary: 'Binary',
        pl.String: 'String',
        pl.Datetime('ms'): "Datetime('ms')",
        pl.Duration('ms'): "Duration('ms')",
        pl.Date: 'Date',
        pl.Time: 'Time',
    }


def serialize_polars_schema(
    schema: pl.schema.Schema | dict[str, mince.types.ColumnType],
) -> list[tuple[str, str]]:
    """convert schema into json-compatible form"""
    import polars as pl

    if isinstance(schema, pl.schema.Schema):
        dict_schema: dict[str, mince.types.ColumnType] = dict(schema.items())
    elif isinstance(schema, dict):
        dict_schema = schema  # type: ignore
    else:
        raise Exception()

    type_map = get_polars_type_map()
    output = []
    for k, v in dict_schema.items():
        v_str = type_map.get(v)
        if v_str is not None:
            output.append((k, v_str))
        else:
            raise Exception('unknown column type: ' + str(v))

    return output


def deserialize_polars_schema(
    schema: typing.Sequence[typing.Sequence[str]],
) -> dict[str, mince.types.ColumnType]:
    """convert json-compatible schema into proper schema"""
    type_map = get_polars_type_map()
    reverse_type_map = {v: k for k, v in type_map.items()}
    output = {}
    for entry in schema:
        if len(entry) != 2:
            raise Exception('invalid schema structure')
        column_name, str_column_type = entry

        column_type = reverse_type_map.get(str_column_type)
        if column_type is None:
            raise Exception()
        output[column_name] = column_type

    return output
