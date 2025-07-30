from __future__ import annotations

from typing import Any, Literal, Protocol, Union
from typing_extensions import TypedDict, NotRequired
from .dashboards import Dashboard  # noqa: F401

import polars as pl
import tooltime


#
# # schema specification
#

Interval = Literal['point', 'day', 'week', 'month', 'year']

ColumnType = Union[pl.datatypes.classes.DataTypeClass, pl.datatypes.DataType]


class DataSchema(TypedDict):
    columns: dict[str, ColumnType]
    group_columns: list[str]


class DataSchemaPartial(TypedDict, total=False):
    columns: dict[str, ColumnType | None] | list[str]
    group_columns: list[str]


class MetricSpec(TypedDict):
    unit: str | None
    type: Literal[
        'point_in_time',
        'sum',
        'min',
        'max',
        'unique',
    ]


#
# # collection specification
#


class CollectKwargs(TypedDict):
    data_dir: str
    start_time: float
    end_time: float
    intervals: list[Interval]
    skip_incomplete_intervals: bool
    extra_kwargs: dict[str, Any]
    dry: bool
    verbose: int


class CollectKwargsPartial(TypedDict, total=False):
    data_dir: str | None
    start_time: tooltime.Timestamp | None
    end_time: tooltime.Timestamp | None
    intervals: list[Interval] | None
    skip_incomplete_intervals: bool | None
    extra_kwargs: dict[str, Any] | None
    extra_kwargs_update: dict[str, Any] | None
    dry: bool | None
    verbose: int | None


class CollectionJobSummary(TypedDict):
    mince_version: str
    dashboard_version: str
    dashboard_name: str
    dashboard_class: str
    job_start_time: float
    job_end_time: float
    data_names: list[str]
    collect_kwargs: CollectKwargs


class AsyncDfCollector(Protocol):
    async def __call__(
        self,
        start_time: int,
        end_time: int,
        interval: Interval,
        tags: dict[str, str],
    ) -> pl.DataFrame: ...


# # ui spec
#

StateDatum = Union[str, int, float]


class UiSpec(TypedDict):
    name: str
    title: str | None  # shown in browser tab title
    description: str | None  # shown in metadata and cli
    favicon_emoji: str | None  # single character str
    version: str
    metrics: dict[str, MetricSpec]
    groupings: list[str]
    default_state: dict[str, StateDatum | None]
    invalid_states: list[dict[str, StateDatum]]
    inputs: dict[str, InputSpec]
    submetrics: dict[str, list[str]]
    shortcuts: dict[str, ShortcutSpec]
    colors: dict[str, str]
    schema: DataSchema
    title_prefix: str | None
    title_infix: str | None
    title_postfix: str | None


class InputSpec(TypedDict):
    type: Literal['button', 'date']
    description: str
    default: str | None
    visibility: NotRequired[InputVisibility]
    button_options: NotRequired[list[str]]
    aliases: dict[str, StateDatum]


class InputVisibility(TypedDict):
    start_hidden: NotRequired[bool]
    hide_if: NotRequired[list[dict[str, Any]]]
    show_if: NotRequired[list[dict[str, Any]]]
    hide: NotRequired[bool]
    f: NotRequired[Any]  # function


class ShortcutSpec(TypedDict):
    action: Literal[
        'select',
        'cycle_next',
        'cycle_previous',
        'toggle_ui',
        'increment',
        'decrement',
    ]
    field: str | None
    value: NotRequired[str]
    help: NotRequired[str]


#
# # registry types
#

RegistryReference = Union['Registry', 'RegistryFile', str, None]


class Registry(TypedDict):
    mince_version: str
    dashboards: dict[str, 'RegistryEntry']


class RegistryFile(TypedDict):
    path: str | None
    validate: NotRequired[bool]
    create_if_dne: NotRequired[bool]


class RegistryEntry(TypedDict):
    name: str
    dashboard_class: str
    description: str | None
    collect_kwargs: CollectKwargsPartial


#
# # validation
#


def validate_typeddict(typed_dict: Any, td_class: type) -> None:
    annotations = td_class.__annotations__

    for field_name, field_type in annotations.items():
        if field_name not in typed_dict:
            raise ValueError(f'Missing required field: {field_name}')

        value = typed_dict[field_name]

        if field_type == pl.DataType:
            if not isinstance(value, pl.DataType):
                raise TypeError(f'Field {field_name} must be a polars DataType')
        elif isinstance(field_type, type):
            if not isinstance(value, field_type):
                raise TypeError(
                    f'Field {field_name} must be of type {field_type}'
                )
        else:
            # Handle more complex types (e.g., Union, List, etc.) here
            # This might require more sophisticated type checking
            pass

    # Check for extra fields
    extra_fields = set(typed_dict.keys()) - set(annotations.keys())
    if extra_fields:
        raise ValueError(f"Unexpected extra fields: {', '.join(extra_fields)}")
