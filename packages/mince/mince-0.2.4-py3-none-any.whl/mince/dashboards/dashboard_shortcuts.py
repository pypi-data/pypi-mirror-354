from __future__ import annotations

from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    import datetime

    import dash_extensions  # type: ignore
    import dash_bootstrap_components as dbc  # type: ignore
    import tooltime

    from mince import types


time_increments = {
    'all': {
        'large': '365d',
        'medium': '30d',
        'small': '7d',
    },
    '365d': {
        'large': '365d',
        'medium': '30d',
        'small': '7d',
    },
    '30d': {
        'large': '30d',
        'medium': '7d',
        'small': '1d',
    },
    '7d': {
        'large': '7d',
        'medium': '1d',
        'small': '1d',
    },
}


def _create_shortcuts_listeners(
    shortcuts: dict[str, types.ShortcutSpec],
) -> dash_extensions.Keyboard:
    import dash_extensions

    return dash_extensions.Keyboard(
        captureKeys=list(shortcuts.keys()), id='keyboard', n_keydowns=1
    )


def _create_help_modal(
    shortcuts: dict[str, types.ShortcutSpec],
) -> dbc.Modal:
    from dash import html  # type: ignore
    import dash_bootstrap_components as dbc

    rows = []
    for key, shortcut in shortcuts.items():
        field = shortcut['field']
        if field is not None:
            field = field.replace('_', ' ')
        # get description
        if 'help' in shortcut:
            description = shortcut['help']
        elif shortcut['action'] == 'toggle_ui':
            description = 'toggle ' + str(shortcut['field'])
        elif shortcut['action'] == 'select':
            description = html.Div(
                ['set ', field, ' to ', html.B(shortcut['value'])]
            )
        elif shortcut['action'] == 'cycle_next':
            description = html.Div(['go to next ', html.B(field)])
        elif shortcut['action'] == 'cycle_previous':
            description = html.Div(['go to previous ', html.B(field)])
        else:
            raise Exception('invalid shortcut action')

        # get key string
        if key == 'ArrowRight':
            key_str = '→'
        elif key == 'ArrowLeft':
            key_str = '←'
        else:
            key_str = key

        # build table row
        row = [
            html.Td(' '),
            html.Td(html.B(key_str)),
            html.Td(' '),
            html.Td(' '),
            html.Td(' '),
            html.Td(description),
            html.Td(' '),
        ]
        rows.append(row)

    return dbc.Modal(
        [
            dbc.ModalHeader(dbc.ModalTitle('Keyboard Shortcuts')),
            dbc.ModalBody(
                html.Table(html.Tbody([html.Tr(row) for row in rows])),
            ),
        ],
        id='help-modal',
        size='sm',
        is_open=False,
    )


def _process_keyboard_shortcuts(
    display_state: dict[str, Any],
    # help_open: bool,
    ui_state: dict[str, Any],
    raw_shortcut: dict[str, Any],
    data_date_range: tuple[tooltime.Timestamp, tooltime.Timestamp],
    ui_spec: types.UiSpec,
) -> None:
    import tooltime

    shortcut = ui_spec['shortcuts'][raw_shortcut['key']]
    field = shortcut['field']
    if shortcut['action'] == 'select' and field is not None:
        display_state[field] = shortcut['value']
    elif shortcut['action'] == 'cycle_next' and field is not None:
        options = ui_spec['inputs'][field]['button_options']
        index = options.index(display_state[field])
        if index + 1 == len(options):
            display_state[field] = options[0]
        else:
            display_state[field] = options[index + 1]
    elif shortcut['action'] == 'cycle_previous' and field is not None:
        options = ui_spec['inputs'][field]['button_options']
        index = options.index(display_state[field])
        if index == 0:
            display_state[field] = options[-1]
        else:
            display_state[field] = options[index - 1]
    elif (
        shortcut['action'] in ['increment', 'decrement']
        and shortcut['field'] == 'now'
    ):
        if raw_shortcut['ctrlKey'] or raw_shortcut['shiftKey']:
            value = 'medium'
        elif raw_shortcut['ctrlKey'] and raw_shortcut['shiftKey']:
            value = 'small'
        else:
            value = 'large'

        duration = time_increments[display_state['time_window']][value]
        new_now_dt = tooltime.timestamp_to_datetime(display_state['now'][:10])
        if shortcut['action'] == 'increment':
            new_now_dt = _increment_datetime(new_now_dt, duration)
        elif shortcut['action'] == 'decrement':
            new_now_dt = _decrement_datetime(new_now_dt, duration)
        else:
            raise Exception()
        new_now = tooltime.timestamp_to_date(new_now_dt)

        # check that new time is valid
        min_now = tooltime.timestamp_to_date(data_date_range[0])
        if new_now < min_now:
            new_now = min_now
        max_now = tooltime.timestamp_to_date(data_date_range[1])
        if new_now > max_now:
            new_now = max_now

        display_state['now'] = new_now
    elif shortcut['action'] == 'toggle_ui':
        field = shortcut['field']
        if field is None:
            raise Exception('no field for shortcut')
        ui_state[field] = not ui_state[field]
    else:
        raise Exception('invalid shortcut action')


def _increment_datetime(
    dt: datetime.datetime, duration: str
) -> datetime.datetime:
    import datetime

    if duration == '1d':
        return dt + datetime.timedelta(days=1)
    elif duration == '7d':
        return dt + datetime.timedelta(days=7)
    elif duration == '30d':
        if dt.month == 12:
            return dt.replace(month=1, year=dt.year + 1)
        else:
            return dt.replace(month=dt.month + 1)
    elif duration == '365d':
        return dt.replace(year=dt.year + 1)
    else:
        raise Exception('invalid increment')


def _decrement_datetime(
    dt: datetime.datetime, duration: str
) -> datetime.datetime:
    import datetime

    if duration == '1d':
        return dt - datetime.timedelta(days=1)
    elif duration == '7d':
        return dt - datetime.timedelta(days=7)
    elif duration == '30d':
        if dt.month == 1:
            return dt.replace(month=12, year=dt.year - 1)
        else:
            return dt.replace(month=dt.month - 1)
    elif duration == '365d':
        return dt.replace(year=dt.year - 1)
    else:
        raise Exception('invalid increment')
