from __future__ import annotations

import typing

from . import spec_validate

if typing.TYPE_CHECKING:
    from typing import Mapping, Sequence, Union
    from mince.types import (
        StateDatum,
        InputSpec,
        UiSpec,
        ShortcutSpec,
        MetricSpec,
        DataSchema,
    )


def create_ui_spec(
    *,
    name: str,
    title: str | None,
    description: str | None,
    favicon_emoji: str | None = None,
    version: str,
    invalid_states: Sequence[Mapping[str, StateDatum]],
    inputs: Mapping[str, InputSpec],
    metrics: dict[str, MetricSpec],
    groupings: list[str],
    submetrics: Mapping[str, Sequence[str]],
    shortcuts: Mapping[str, ShortcutSpec],
    colors: Mapping[str, str],
    schema: DataSchema,
    title_prefix: str | None,
    title_infix: str | None,
    title_postfix: str | None,
) -> UiSpec:
    default_state: dict[str, Union[str, int, float] | None] = {
        input: input_spec['default'] for input, input_spec in inputs.items()
    }

    ui_spec: UiSpec = {
        'name': name,
        'title': title,
        'description': description,
        'favicon_emoji': favicon_emoji,
        'version': version,
        'groupings': groupings,
        'default_state': default_state,
        'invalid_states': [dict(item) for item in invalid_states],
        'inputs': dict(inputs),
        'metrics': metrics,
        'submetrics': {k: list(v) for k, v in submetrics.items()},
        'shortcuts': dict(shortcuts),
        'colors': dict(colors),
        'schema': schema,
        'title_prefix': title_prefix,
        'title_infix': title_infix,
        'title_postfix': title_postfix,
    }

    spec_validate.validate_ui_spec(ui_spec)

    return ui_spec
