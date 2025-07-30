from __future__ import annotations

import argparse
import typing

import mince
from ... import storage
from .. import cli_helpers
from .. import cli_parsing

if typing.TYPE_CHECKING:
    from mince import types


def add_unregister_command(
    subparsers: cli_helpers.Subparsers,
    include_dashboard_arg: bool,
    DashboardClass: typing.Type[mince.Dashboard] | None,
) -> None:
    parser = subparsers.add_parser(
        'unregister',
        help='unregister dashboard',
        formatter_class=cli_helpers.HelpFormatter,
    )
    parser.set_defaults(f_command=unregister_command)
    if include_dashboard_arg:
        parser.add_argument(
            'dashboard',
            help='dashboard to unregister',
        )
    cli_parsing.add_common_args(parser)


def unregister_command(
    args: argparse.Namespace,
    dashboard: str | typing.Type[types.Dashboard] | None = None,
) -> None:
    if dashboard is None:
        dashboard = args.dashboard
    storage.unregister_dashboard(
        name=dashboard,
        path=args.registry,
        validate=not args.no_validate,
    )
    print('dashboard', dashboard, 'unregistered')
