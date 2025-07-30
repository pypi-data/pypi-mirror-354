from __future__ import annotations

import argparse
import typing

from ... import storage
from .. import cli_helpers
from .. import cli_parsing

if typing.TYPE_CHECKING:
    from mince import types


def add_data_command(
    subparsers: cli_helpers.Subparsers,
    include_dashboard_arg: bool,
    DashboardClass: typing.Type[types.Dashboard] | None,
) -> None:
    parser = subparsers.add_parser(
        'data',
        help='view dashboard data',
        formatter_class=cli_helpers.HelpFormatter,
    )
    parser.set_defaults(f_command=data_command)
    if include_dashboard_arg:
        parser.add_argument(
            'dashboard',
            help='dashboard to get data of',
        )
    parser.add_argument(
        '-i',
        '--interactive',
        help='load data in interactive python session',
        action='store_true',
    )
    cli_parsing.add_common_args(parser)


def data_command(
    args: argparse.Namespace,
    dashboard: str | typing.Type[types.Dashboard] | None = None,
) -> None:
    if dashboard is None:
        dashboard = args.dashboard
    data_dir = storage.resolve_data_dir(
        dashboard=dashboard,
        registry={'path': args.registry, 'validate': not args.no_validate},
    )
    job, dfs = storage.load_dashboard_data(data_dir=data_dir)

    if args.interactive:
        cli_helpers.open_interactive_session(variables=dfs)
    else:
        first = True
        for key, df in dfs.items():
            print()
            if first:
                first = False
            else:
                print()
            print('name =', key)
            print(df)
