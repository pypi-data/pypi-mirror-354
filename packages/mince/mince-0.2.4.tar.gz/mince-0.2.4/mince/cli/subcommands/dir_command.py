from __future__ import annotations

import argparse
import typing

from .. import cli_helpers
from .. import cli_parsing
from . import cd_command

if typing.TYPE_CHECKING:
    from mince import types


def add_dir_command(
    subparsers: cli_helpers.Subparsers,
    include_dashboard_arg: bool,
    DashboardClass: typing.Type[types.Dashboard] | None,
) -> None:
    parser = subparsers.add_parser(
        'dir',
        help='print mince root or dashboard data directory',
        formatter_class=cli_helpers.HelpFormatter,
    )
    parser.set_defaults(f_command=dir_command)
    if include_dashboard_arg:
        parser.add_argument('dashboard', help='dashboard name', nargs='?')
    parser.add_argument(
        '--code', help='print dir of code directory', action='store_true'
    )
    cli_parsing.add_common_args(parser)


def dir_command(
    args: argparse.Namespace,
    dashboard: str | typing.Type[types.Dashboard] | None = None,
) -> None:
    if dashboard is None:
        dashboard = args.dashboard
    path = cd_command.get_path(args, dashboard)
    print(path)
