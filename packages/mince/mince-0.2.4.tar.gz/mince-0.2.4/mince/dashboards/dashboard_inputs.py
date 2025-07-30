from __future__ import annotations

from typing import Any, Sequence, TYPE_CHECKING


if TYPE_CHECKING:
    from dash import html, dcc, Dash  # type: ignore
    import tooltime
    from mince import types


def create_inputs(
    ui_spec: types.UiSpec,
    date_range: tuple[tooltime.Timestamp, tooltime.Timestamp],
) -> dict[str, html.Div]:
    from dash import html

    inputs: dict[str, html.Div] = {}
    for name, input_spec in ui_spec['inputs'].items():
        if input_spec['type'] == 'button':
            inputs[name] = create_button(name=name, input_spec=input_spec)
        elif input_spec['type'] == 'date':
            inputs[name] = create_date_picker(input_spec, date_range)
        else:
            raise Exception('invalid input type')
    return inputs


def create_button(name: str, input_spec: types.InputSpec) -> html.Div:
    start_hidden = input_spec.get('visibility', {}).get('start_hidden', False)
    return create_radio_group(
        name=name,
        options=input_spec['button_options'],
        default=input_spec['default'],
        description=input_spec['description'],
        start_hidden=start_hidden,
    )


def create_radio_group(
    name: str,
    options: Sequence[str],
    default: str | None = None,
    start_hidden: bool = False,
    description: str | None = None,
) -> html.Div:
    """create a radio button group"""
    from dash import html
    import dash_bootstrap_components as dbc  # type: ignore

    if default is None:
        default = options[0]

    if start_hidden:
        default_className = 'btn-group hidden'
    else:
        default_className = 'btn-group'

    return html.Div(
        [
            dbc.RadioItems(
                id=name + '-radio',
                className=default_className,
                inputClassName='btn-check',
                labelClassName='btn btn-outline-dark',
                labelCheckedClassName='active',
                options=[
                    {'label': option, 'value': option} for option in options
                ],
                value=default,
            ),
            dbc.Popover(
                description,
                target=name + '-radio',
                body=True,
                trigger='hover',
                placement='bottom',
            ),
        ],
        className='radio-group',
    )


def create_date_picker(
    input_spec: types.InputSpec,
    date_range: tuple[tooltime.Timestamp, tooltime.Timestamp],
) -> dcc.DatePickerSingle:
    from dash import html, dcc
    import dash_bootstrap_components as dbc
    import tooltime

    start_time, end_time = date_range
    min_date = tooltime.timestamp_to_datetime(start_time).strftime('%Y-%m-%d')
    max_date = tooltime.timestamp_to_datetime(end_time).strftime('%Y-%m-%d')
    return html.Div(
        [
            dcc.DatePickerSingle(
                id='date-picker',
                min_date_allowed=min_date,
                max_date_allowed=max_date,
                initial_visible_month=max_date,
                date=max_date,
                display_format='Y-MM-DD',
            ),
            dbc.Popover(
                input_spec['description'],
                target='date-picker',
                body=True,
                trigger='hover',
                placement='bottom',
            ),
        ],
        className='dash-bootstrap',
    )


def _prevent_button_focus(app: Dash) -> None:
    # this function is run to prevent radio buttons from being focus-able
    # otherwise, they conflict with the shortcuts used for the arrow keys
    from dash import Input, Output

    app.clientside_callback(
        """
        function(trigger) {
            if (!window.preventFocusApplied) {
                function preventFocus() {
                    document.querySelectorAll('.radio-group input[type="radio"]').forEach(radio => {
                        radio.addEventListener('focus', (e) => e.target.blur());
                    });
                }
                preventFocus();
                window.preventFocusApplied = true;
            }
            return '';
        }
        """,
        Output('prevent-focus-trigger', 'children'),
        Input('prevent-focus-trigger', 'children'),
    )


#
# # visibility
#


def compute_input_classes(
    state: dict[str, Any],
    ui_spec: types.UiSpec,
) -> dict[str, str]:
    classes = {True: 'btn-group', False: 'btn-group hidden'}
    return {
        name: classes[is_visible(state, input_spec)]
        for name, input_spec in ui_spec['inputs'].items()
    }


def is_visible(state: dict[str, Any], input_spec: types.InputSpec) -> bool:
    visibility = input_spec.get('visibility')
    if visibility is None:
        return True
    if visibility.get('hide'):
        return False
    if 'show_if' in visibility:
        if not any(is_match(state, match) for match in visibility['show_if']):
            return False
    elif 'hide_if' in input_spec['visibility']:
        if any(is_match(state, match) for match in visibility['hide_if']):
            return False
    return True


def is_match(display: dict[str, str], match: dict[str, str]) -> bool:
    for key, value in match.items():
        if display.get(key) != value:
            return False
    return True
