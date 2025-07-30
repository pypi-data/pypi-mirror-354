from __future__ import annotations

import typing

from mince import specs

if typing.TYPE_CHECKING:
    from mince import types


def get_df_metric(state: dict[str, str], ui_spec: types.UiSpec) -> str:
    if state['metric'] in ui_spec['submetrics']:
        return state['submetric']
    else:
        return state['metric']


def build_state(
    *,
    _ui_spec: types.UiSpec,
    _defaults: bool = False,
    _fix: bool = True,
    _validate: bool = True,
    **kwargs: typing.Any,
) -> dict[str, str]:
    import tooltime

    _replace_aliased_values(kwargs, ui_spec=_ui_spec)
    state = dict(**kwargs)

    if _defaults:
        for key, value in _ui_spec['default_state'].items():
            if key not in state:
                state[key] = value
        if 'now' not in state:
            state['now'] = tooltime.now()

    if _fix or _validate:
        if _fix:
            _fix_invalid_option_combinations(state, _ui_spec)
        elif _validate:
            invalid_combos = _find_invalid_option_combinations(state, _ui_spec)
            if invalid_combos is not None:
                raise Exception(
                    'invalid combination of state: ' + str(invalid_combos)
                )
        invalid_values = _find_invalid_option_values(state, _ui_spec)
        if len(invalid_values) > 0:
            raise Exception('invalid option values: ' + str(invalid_values))

    return state


def _replace_aliased_values(
    combo: dict[str, types.StateDatum | None],
    ui_spec: types.UiSpec,
) -> None:
    for key, value in combo.items():
        if value in ui_spec['inputs'][key]['aliases']:
            if isinstance(value, str):
                combo[key] = ui_spec['inputs'][key]['aliases'][value]


def _fix_invalid_option_combinations(
    state: dict[str, types.StateDatum | None],
    ui_spec: types.UiSpec,
    freeze_fields: list[str] | None = None,
    aliased: bool = False,
) -> None:
    while True:
        invalid = _find_invalid_option_combinations(state, ui_spec)
        if invalid is None:
            return
        for key in invalid.keys():
            if freeze_fields is not None and key not in freeze_fields:
                state[key] = ui_spec['default_state'][key]


def _fix_invalid_inputs(
    state: dict[str, types.StateDatum | None],
    raw_shortcut: dict[str, typing.Any],
    ui_spec: types.UiSpec,
) -> None:
    from dash import callback_context  # type: ignore

    # determine origin of trigger
    ctx = callback_context
    triggered_input = ctx.triggered[0]['prop_id'].split('.')[0]

    # get shortcut spec
    if raw_shortcut is not None:
        shortcut = ui_spec['shortcuts'][raw_shortcut['key']]
    else:
        shortcut = {}

    # fix time_window too small for sample_interval too small
    _ensure_time_window_exceeds_sample_interval(
        state, triggered_input, shortcut
    )

    # check invalid option combinations
    trigger = triggered_input.split('-radio')[0]

    _fix_invalid_option_combinations(
        state, freeze_fields=[trigger], aliased=True, ui_spec=ui_spec
    )


def _ensure_time_window_exceeds_sample_interval(
    values: dict[str, types.StateDatum | None],
    trigger: str,
    shortcut: types.ShortcutSpec,
) -> None:
    if values['time_window'] == '7d' and values['sample_interval'] == 'weekly':
        if trigger == 'time_window-radio':
            values['sample_interval'] = 'daily'
        elif trigger == 'sample_interval-radio':
            values['time_window'] = '30d'
        elif trigger == 'keyboard' and shortcut['field'] == 'sample_interval':
            values['time_window'] = '30d'
        else:
            values['sample_interval'] = 'daily'
    elif (
        values['time_window'] == '7d' and values['sample_interval'] == 'monthly'
    ):
        if trigger == 'time_window-radio':
            values['sample_interval'] = 'daily'
        elif trigger == 'sample_interval-radio':
            values['time_window'] = '365d'
        elif trigger == 'keyboard' and shortcut['field'] == 'sample_interval':
            values['time_window'] = '365d'
        else:
            values['sample_interval'] = 'daily'
    elif (
        values['time_window'] == '30d'
        and values['sample_interval'] == 'monthly'
    ):
        if trigger == 'time_window-radio':
            values['sample_interval'] = 'weekly'
        elif trigger == 'sample_interval-radio':
            values['time_window'] = '365d'
        elif trigger == 'keyboard' and shortcut['field'] == 'sample_interval':
            values['time_window'] = '365d'
        else:
            values['sample_interval'] = 'weekly'


def _find_invalid_option_combinations(
    state: dict[str, types.StateDatum | None],
    ui_spec: types.UiSpec,
    aliased: bool = False,
) -> dict[str, typing.Any] | None:
    if aliased:
        state = state.copy()
        _replace_aliased_values(state, ui_spec)
    for value in ui_spec['invalid_states']:
        if all(state[k] == v for k, v in value.items()):
            return value
    return None


def _find_invalid_option_values(
    state: dict[str, str],
    ui_spec: types.UiSpec,
) -> dict[str, typing.Any]:
    output = {}
    for key, value in state.items():
        if ui_spec['inputs'][key]['type'] == 'button':
            valid_values = [
                specs.alias_to_state(option, key, ui_spec)
                for option in ui_spec['inputs'][key]['button_options']
            ]
        elif ui_spec['inputs'][key]['type'] == 'date':
            continue
        else:
            raise Exception('invalid type')

        if value not in valid_values:
            print('VALID VALUES:', valid_values, 'ACTUAL:', value, 'FOR:', key)
            output[key] = value
    return output
