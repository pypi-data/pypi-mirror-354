from __future__ import annotations

import argparse
import typing

import mince.ops
from .. import cli_helpers
from .. import cli_parsing

if typing.TYPE_CHECKING:
    from mince import types


def add_kill_command(
    subparsers: cli_helpers.Subparsers,
    include_dashboard_arg: bool,
    DashboardClass: typing.Type[mince.Dashboard] | None,
) -> None:
    parser = subparsers.add_parser(
        'kill',
        help='kill dashboard',
        formatter_class=cli_helpers.HelpFormatter,
    )
    parser.set_defaults(f_command=kill_command)
    if include_dashboard_arg:
        parser.add_argument('dashboard', help='dashboard name', nargs='?')
    parser.add_argument('--port', help='port number to kill dashboard of')
    parser.add_argument('--pid', help='pid to kill')
    cli_parsing.add_common_args(parser)


def kill_command(
    args: argparse.Namespace,
    dashboard: str | typing.Type[types.Dashboard] | None = None,
) -> None:
    if dashboard is None:
        dashboard = args.dashboard
    if isinstance(dashboard, str):
        mince.ops.kill_server(name=dashboard, port=args.port, pid=args.pid)
    else:
        raise NotImplementedError('cannot kill pure class')
