from __future__ import annotations

import typing

from mince import specs
from . import dashboard_class
from . import dashboard_inputs
from . import dashboard_state
from . import dashboard_urls

if typing.TYPE_CHECKING:
    import flask
    from dash import Dash, Input, Output, State  # type: ignore
    import plotly.graph_objects as go  # type: ignore
    from mince import types


def _create_app(
    dashboard: dashboard_class.Dashboard,
    assets_folder: str | None = None,
    external_stylesheets: list[str] | None = None,
    pdb: bool = False,
) -> Dash:
    """create the dash.Dash object for a DashBoard"""
    from dash import Dash

    if external_stylesheets is None:
        import dash_bootstrap_components as dbc  # type: ignore

        external_stylesheets = [dbc.themes.BOOTSTRAP]

    # create app
    if assets_folder is None:
        assets_folder = get_default_assets_folder()
    app = Dash(
        dashboard.spec['name'],
        assets_folder=assets_folder,
        external_stylesheets=external_stylesheets,
    )
    app.title = dashboard.spec['name']
    favicon_emoji = dashboard.spec.get('favicon_emoji')
    if favicon_emoji is not None:
        app.index_string = app.index_string.replace(
            '{%favicon%}',
            '<link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>'  # noqa: E501
            + favicon_emoji
            + '</text></svg>">',
        )
    n_keydowns = 0

    # create inputs
    inputs = dashboard_inputs.create_inputs(
        dashboard.spec, dashboard.date_range
    )

    # create layout
    app.layout = dashboard.get_layout(inputs)

    # add serverside callbacks
    update_ui_args, update_chart_args = _compute_decorator_args(dashboard.spec)

    @app.callback(*update_ui_args)  # type: ignore
    def update_ui(*args) -> list[str | bool]:
        # parse input args
        (
            *raw_display_state,
            url,
            initial_load,
            _n_keydowns,
            shortcut,
            help_open,
            submetric_options,
            radio_group_visibility,
        ) = args
        display_state = dict(zip(list(inputs.keys()), raw_display_state))
        ui_state = {
            'initial_load': initial_load,
            'help_open': help_open,
            'submetric_options': submetric_options,
            'radio_group_visibility': radio_group_visibility,
        }

        # load from url
        if ui_state['initial_load']:
            dashboard_urls.parse_url(
                url, display_state, dashboard.spec['default_state']
            )
            ui_state['initial_load'] = False

        # process keyboard shortcuts
        nonlocal n_keydowns
        if _n_keydowns <= n_keydowns or shortcut is None:
            shortcut = None
        else:
            # help_open =
            dashboard.process_shortcuts(display_state, ui_state, shortcut)
        n_keydowns = _n_keydowns

        # specify submetrics list
        if display_state['metric'] in dashboard.spec['submetrics']:
            raw_options = dashboard.spec['submetrics'][display_state['metric']]
            button_options = []
            submetric_options = []
            for raw_option in raw_options:
                option = specs.state_to_alias(
                    raw_option, 'submetric', dashboard.spec
                )
                button_options.append(option)
                submetric_options.append({'label': option, 'value': option})
            ui_state['submetric_options'] = submetric_options
            dashboard.spec['inputs']['submetric']['button_options'] = (
                button_options
            )
            if display_state['submetric'] not in button_options:
                display_state['submetric'] = button_options[0]

        # based on most recent selection, fix any invalid button values
        dashboard_state._fix_invalid_inputs(
            display_state, shortcut, dashboard.spec
        )

        # update url based on radio button values
        url = dashboard_urls.create_new_url(
            display_state, defaults=dashboard.spec['default_state']
        )

        # update visibility of interval, time, and yscale radio buttons
        raw_classes = dashboard_inputs.compute_input_classes(
            display_state, dashboard.spec
        )
        classes = list(raw_classes.values())

        if ui_state['radio_group_visibility']:
            radio_group_row_class = ''
        else:
            radio_group_row_class = 'hidden'

        return (
            list(display_state.values())
            + classes
            + [
                url,
                ui_state['initial_load'],
                ui_state['help_open'],
                ui_state['submetric_options'],
                ui_state['radio_group_visibility'],
                radio_group_row_class,
            ]
        )

    # add chart callback
    @app.callback(*update_chart_args)  # type: ignore
    def update_chart(*args) -> go.Figure:
        kwargs = dict(zip(inputs.keys(), args))
        kwargs['now'] = kwargs['now'][:10]
        state = dashboard_state.build_state(
            _fix=False, _ui_spec=dashboard.spec, **kwargs
        )
        return dashboard.create_chart(state)

    # add clientside callbacks
    dashboard_inputs._prevent_button_focus(app)

    # Add a new route
    @app.server.route('/metadata')  # type: ignore
    def mince_metadata() -> flask.Response:
        import flask

        return flask.jsonify(dashboard.get_metadata())

    # add interactive debugger
    if pdb:

        @app.server.errorhandler(Exception)  # type: ignore
        def custom_exception_handler(
            e: Exception,
        ) -> tuple[flask.Response, int]:
            import sys
            import flask

            try:
                import ipdb as pdb  # type: ignore
            except ImportError:
                import pdb
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback_details = {
                'filename': exc_traceback.tb_frame.f_code.co_filename,  # type: ignore
                'lineno': exc_traceback.tb_lineno,  # type: ignore
                'name': exc_traceback.tb_frame.f_code.co_name,  # type: ignore
                'type': exc_type.__name__,  # type: ignore
                'message': str(e),
            }
            pdb.post_mortem(exc_traceback)
            return flask.jsonify(error=traceback_details), 500

    return app


def _compute_decorator_args(
    ui_spec: types.UiSpec,
) -> tuple[list[Input | Output | State], list[Input | Output | State]]:
    from dash import Input, Output, State

    dash_input_values = []
    dash_output_values = []
    dash_output_classes = []
    for name, input_spec in ui_spec['inputs'].items():
        if input_spec['type'] == 'button':
            dash_input_values.append(Input(name + '-radio', 'value'))
            dash_output_values.append(Output(name + '-radio', 'value'))
            dash_output_classes.append(Output(name + '-radio', 'className'))
        elif input_spec['type'] == 'date':
            dash_input_values.append(Input('date-picker', 'date'))
            dash_output_values.append(Output('date-picker', 'date'))
            dash_output_classes.append(Output('date-picker', 'className'))
        else:
            raise Exception('invalid type')

    # ui args
    update_ui_args = [
        # outputs
        dash_output_values,
        dash_output_classes,
        [
            Output('url', 'search'),
            Output('initial-load', 'data'),
            Output('help-modal', 'is_open'),
            Output('submetric-radio', 'options'),
            Output('radio-group-visibility', 'data'),
            Output('radio-group-row', 'className'),
        ],
        # inputs
        dash_input_values,
        [
            Input('url', 'search'),
            State('initial-load', 'data'),
            Input('keyboard', 'n_keydowns'),
            State('keyboard', 'keydown'),
            State('help-modal', 'is_open'),
            State('submetric-radio', 'options'),
            State('radio-group-visibility', 'data'),
        ],
    ]

    # chart args
    update_chart_args = [
        Output('main-chart', 'figure'),
        dash_input_values,
    ]

    return update_ui_args, update_chart_args


def get_default_assets_folder() -> str:
    import importlib.resources
    import os

    path = str(
        importlib.resources.path(
            'mince.resources.frontend.assets', 'favicon.ico'
        )
    )
    return os.path.dirname(path)
