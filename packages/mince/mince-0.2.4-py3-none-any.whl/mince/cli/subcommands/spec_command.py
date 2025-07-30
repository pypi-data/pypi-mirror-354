from __future__ import annotations

import argparse
import typing

import mince
from ... import dashboards
from .. import cli_helpers
from .. import cli_parsing

if typing.TYPE_CHECKING:
    from mince import types


def add_spec_command(
    subparsers: cli_helpers.Subparsers,
    include_dashboard_arg: bool,
    DashboardClass: typing.Type[mince.Dashboard] | None,
) -> None:
    parser = subparsers.add_parser(
        'spec',
        help='view dashboard ui specification',
        formatter_class=cli_helpers.HelpFormatter,
    )
    parser.set_defaults(f_command=spec_command)
    if include_dashboard_arg:
        parser.add_argument(
            'dashboard',
            help='dashboard to get UI spec of',
        )
    parser.add_argument(
        '-i',
        '--interactive',
        help='load spec in interactive python session',
        action='store_true',
    )
    cli_parsing.add_common_args(parser)


def spec_command(
    args: argparse.Namespace,
    dashboard: str | typing.Type[types.Dashboard] | None = None,
) -> None:
    registry: types.RegistryFile = {
        'path': args.registry,
        'validate': not args.no_validate,
    }
    if dashboard is None:
        dashboard = args.dashboard
    if isinstance(dashboard, str):
        DashboardClass = dashboards.get_dashboard_class(
            dashboard, registry=registry
        )
    elif issubclass(dashboard, mince.Dashboard):
        DashboardClass = dashboard
    else:
        raise Exception()

    ui_spec = DashboardClass.load_spec()

    if args.interactive:
        cli_helpers.open_interactive_session(variables={'spec': ui_spec})
    else:
        import json

        as_str = json.dumps(
            ui_spec,
            sort_keys=True,
            indent=4,
            cls=cli_helpers.SpecJsonEncoder,
        )
        print(as_str)
