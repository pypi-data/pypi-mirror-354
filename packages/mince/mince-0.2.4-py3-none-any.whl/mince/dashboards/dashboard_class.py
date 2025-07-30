from __future__ import annotations

from typing import Any, TYPE_CHECKING

from mince.figures import ui_figures
from mince import schemas, specs
from . import dashboard_apps
from . import dashboard_shortcuts

if TYPE_CHECKING:
    from typing_extensions import Unpack
    from dash import Dash, html  # type: ignore
    import plotly.graph_objects as go  # type: ignore
    import polars as pl
    import tooltime
    from mince.types import (
        CollectKwargs,
        CollectKwargsPartial,
        CollectionJobSummary,
        UiSpec,
    )


class Dashboard:
    """main object to instantiate or modify when building a dashboard

    the methods exposed in this class are those that may be useful to override
    """

    # class properties

    @classmethod
    def load_spec(cls) -> UiSpec:
        raise NotImplementedError('load_spec() not implemented')

    @classmethod
    async def async_collect_data(
        cls, **kwargs: Unpack[CollectKwargs]
    ) -> dict[str, pl.DataFrame]:
        raise NotImplementedError('async_collect_data() not implemented')

    @classmethod
    def get_default_collect_kwargs(cls) -> CollectKwargsPartial:
        import time

        return {
            'start_time': 0,
            'end_time': int(time.time()),
            'intervals': ['day', 'week', 'month'],
            'skip_incomplete_intervals': False,
            'extra_kwargs': {},
            'extra_kwargs_update': {},
            'verbose': 1,
            'dry': False,
        }

    @classmethod
    def validate(cls, spec: UiSpec, dfs: dict[str, pl.DataFrame]) -> None:
        specs.validate_ui_spec(spec)
        schemas.validate_data_matches_spec(dfs, spec)

    # instance properties

    spec: UiSpec
    dfs: dict[str, pl.DataFrame]
    date_range: tuple[int, int]
    debug: bool
    app: Dash
    t_run_start: float | None
    n_keydowns: int
    job: CollectionJobSummary | None

    def __init__(
        self,
        *,
        dfs: dict[str, pl.DataFrame],
        spec: UiSpec,
        debug: bool = False,
        pdb: bool = False,
        assets_folder: str | None = None,
        date_range: tuple[tooltime.Timestamp, tooltime.Timestamp],
        job: CollectionJobSummary | None = None,
    ):
        import tooltime

        self.validate(dfs=dfs, spec=spec)
        self.spec = spec
        self.spec['default_state']['now'] = tooltime.timestamp_to_date(
            date_range[1]
        )
        self.dfs = dfs
        self.debug = debug
        self.mince_version = specs.get_package_version('mince')
        start_time, end_time = date_range
        self.date_range = (
            tooltime.timestamp_to_seconds(start_time),
            tooltime.timestamp_to_seconds(end_time),
        )
        self.app = dashboard_apps._create_app(
            dashboard=self, assets_folder=assets_folder, pdb=pdb
        )
        self.job = job
        self.n_keydowns = 0
        self.t_run_start = None

    def run(
        self,
        port: str | int | None = None,
        jupyter_mode: str = 'external',
        **kwargs: Any,
    ) -> None:
        import time
        import mince.ops

        if port is None:
            port = str(mince.ops.find_available_port(8052))
        else:
            port = str(port)
        self.t_run_start = time.time()

        try:
            mince.ops.create_pid_file(dashboard=self, port=port)
            self.app.run(
                host='0.0.0.0', jupyter_mode=jupyter_mode, port=port, **kwargs
            )
        finally:
            mince.ops.clear_pid_file(dashboard=self, port=port)

    def get_metadata(self) -> dict[str, Any]:
        import tooltime

        if self.t_run_start is not None:
            t_run_start = tooltime.timestamp_to_iso_pretty(self.t_run_start)
        else:
            t_run_start = None
        return {
            'mince_version': self.mince_version,
            'dashboard_version': self.spec['version'],
            'name': self.spec['name'],
            'description': self.spec['description'],
            'time_started': t_run_start,
            'job': self.job,
        }

    def get_layout(self, inputs: dict[str, html.Div]) -> list[html.Div]:
        from dash import dcc, html

        return [
            dashboard_shortcuts._create_shortcuts_listeners(
                self.spec['shortcuts']
            ),
            dcc.Location(id='url', refresh=False),
            dcc.Store(id='initial-load', data=True),
            dcc.Store(id='radio-group-visibility', data=True),
            html.Div(list(inputs.values()), id='radio-group-row'),
            dcc.Graph(
                id='main-chart',
                config={
                    'responsive': True,
                    'displayModeBar': True,
                    'displaylogo': False,
                    'modeBarButtonsToRemove': [
                        'select2d',
                        'lasso2d',
                        'zoom',
                        'pan',
                        'zoomIn',
                        'zoomOut',
                        'autoScale',
                        'resetScale',
                    ],
                    'modeBarButtonsToAdd': ['toImage'],
                },
            ),
            dashboard_shortcuts._create_help_modal(self.spec['shortcuts']),
            html.Div(id='prevent-focus-trigger'),
        ]

    def get_dataset(self, state: dict[str, Any]) -> str:
        if len(self.dfs) == 1:
            return next(iter(self.dfs.keys()))
        else:
            raise NotImplementedError('get_dataset()')

    def process_shortcuts(
        self,
        display_state: dict[str, Any],
        ui_state: dict[str, Any],
        raw_shortcut: dict[str, Any],
    ) -> None:
        dashboard_shortcuts._process_keyboard_shortcuts(
            display_state=display_state,
            ui_state=ui_state,
            raw_shortcut=raw_shortcut,
            data_date_range=self.date_range,
            ui_spec=self.spec,
        )

    def create_chart(self, state: dict[str, Any]) -> go.Figure:
        data_name = self.get_dataset(state)
        df = self.dfs[data_name]

        title = self.create_title(
            df=df,
            state=state,
            data_date_range=self.date_range,
            ui_spec=self.spec,
        )

        if state['format'] in ['line', 'line %', 'area', 'area %']:
            return ui_figures.create_time_series_fig(
                df, state, self.debug, ui_spec=self.spec, title=title
            )
        elif state['format'] == 'tree':
            return ui_figures.create_treemap_fig(
                df,
                state,
                ui_spec=self.spec,
                data_date_range=self.date_range,
                title=title,
            )
        else:
            raise Exception('invalid format: ' + str(state['format']))

    def create_title(
        self,
        df: pl.DataFrame,
        state: dict[str, Any],
        data_date_range: tuple[int, int],
        ui_spec: UiSpec,
    ) -> str | None:
        return None
