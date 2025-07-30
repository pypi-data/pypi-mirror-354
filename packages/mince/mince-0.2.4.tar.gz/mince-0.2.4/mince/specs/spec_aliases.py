from __future__ import annotations

import typing

if typing.TYPE_CHECKING:
    from mince.types import StateDatum, UiSpec


def alias_to_state(
    value: str, field: str, ui_spec: UiSpec, *, require: bool = False
) -> StateDatum:
    aliases = ui_spec['inputs'][field]['aliases']
    if value in aliases:
        return aliases[value]
    elif require:
        raise Exception('invalid alias: ' + str(value))
    else:
        return value


def state_to_alias(
    value: StateDatum, field: str, ui_spec: UiSpec, *, require: bool = False
) -> str:
    aliases = ui_spec['inputs'][field]['aliases']
    for alias_value, state_value in aliases.items():
        if value == state_value:
            return alias_value
    if require:
        raise Exception('no alias for state value: ' + str(value))
    else:
        return str(value)
