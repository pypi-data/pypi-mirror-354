from __future__ import annotations

import argparse
import typing

import mince
from ... import ops
from .. import cli_helpers
from .. import cli_parsing

if typing.TYPE_CHECKING:
    from mince import types


def add_run_command(
    subparsers: cli_helpers.Subparsers,
    include_dashboard_arg: bool,
    DashboardClass: typing.Type[mince.Dashboard] | None,
) -> None:
    parser = subparsers.add_parser(
        'run',
        help='run dashboard',
        formatter_class=cli_helpers.HelpFormatter,
    )
    parser.set_defaults(f_command=run_command)
    if include_dashboard_arg:
        parser.add_argument(
            'dashboard',
            help='dashboard to run',
        )
    parser.add_argument(
        '--port',
        help='port number to run dashboard on',
    )
    cli_parsing.add_common_args(parser)


def run_command(
    args: argparse.Namespace,
    dashboard: str | typing.Type[types.Dashboard] | None = None,
) -> None:
    registry: types.RegistryFile = {
        'path': args.registry,
        'validate': not args.no_validate,
    }
    if dashboard is None:
        dashboard = args.dashboard
    ops.run_dashboard(
        dashboard=dashboard,
        registry=registry,
        run_kwargs={'port': args.port},
        instance_kwargs={'pdb': args.pdb},
    )
