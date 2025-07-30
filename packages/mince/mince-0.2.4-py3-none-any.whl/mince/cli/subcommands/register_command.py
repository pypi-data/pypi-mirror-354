from __future__ import annotations

import argparse
import typing

import mince
from ... import storage
from .. import cli_helpers
from .. import cli_parsing

if typing.TYPE_CHECKING:
    from mince import types


def add_register_command(
    subparsers: cli_helpers.Subparsers,
    include_dashboard_arg: bool,
    DashboardClass: typing.Type[mince.Dashboard] | None,
) -> None:
    parser = subparsers.add_parser(
        'register',
        help='register dashboard',
        formatter_class=cli_helpers.HelpFormatter,
    )
    parser.set_defaults(f_command=register_command)
    parser.add_argument(
        'dashboard_class',
        metavar='MODULE:CLASS',
        help='Dashboard class',
    )
    cli_parsing.add_common_args(parser)


def register_command(
    args: argparse.Namespace,
    dashboard: str | typing.Type[types.Dashboard] | None = None,
) -> None:
    registry: types.RegistryFile = {
        'path': args.registry,
        'validate': not args.no_validate,
    }
    if dashboard is None:
        dashboard = args.dashboard_class
    storage.register_dashboard(
        dashboard=dashboard,
        registry=registry,
    )
