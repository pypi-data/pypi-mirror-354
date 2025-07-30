from __future__ import annotations

import typing
import importlib
import argparse

import mince
from . import cli_helpers


def parse_args(
    subcommands: list[str],
    include_dashboard_arg: bool,
    DashboardClass: typing.Type[mince.Dashboard] | None,
) -> argparse.Namespace:
    if DashboardClass is None:
        try:
            DashboardClass = parse_dashboard()
        except (SystemExit, KeyError):
            DashboardClass = None

    parser = argparse.ArgumentParser(
        formatter_class=cli_helpers.HelpFormatter, allow_abbrev=False
    )

    # add commands
    subparsers = parser.add_subparsers(dest='command')
    for command in subcommands:
        module_name = 'mince.cli.subcommands.' + command + '_command'
        module = importlib.import_module(module_name)
        arg_adder = getattr(module, 'add_' + command + '_command')
        arg_adder(
            subparsers,
            include_dashboard_arg=include_dashboard_arg,
            DashboardClass=DashboardClass,
        )

    # parse args
    args = parser.parse_args()

    if args.command is None:
        import sys

        parser.print_help()
        sys.exit(0)

    return args


def parse_dashboard() -> typing.Type[mince.Dashboard] | None:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('command')
    parser.add_argument('dashboard', nargs='?')
    add_common_args(parser)
    args, extras = parser.parse_known_args()
    dashboard_name = args.dashboard
    if dashboard_name is not None:
        registry: mince.RegistryFile = {
            'path': args.registry,
            'validate': not args.no_validate,
        }
        DashboardClass = mince.dashboards.get_dashboard_class(
            name=dashboard_name, registry=registry
        )
        return DashboardClass
    else:
        return None


def add_common_args(
    parser: argparse.ArgumentParser, registry_name: str = '--registry'
) -> None:
    parser.add_argument(
        registry_name,
        metavar='PATH',
        help='path to mince registry',
    )
    parser.add_argument(
        '--no-validate',
        help='skip validation of registry',
        action='store_true',
    )
    parser.add_argument(
        '--debug',
        help='use debug mode',
        action='store_true',
    )
    parser.add_argument(
        '--pdb',
        help='use interactive debugger',
        action='store_true',
    )
    parser.add_argument(
        '--cd-destination-tempfile',
        help=argparse.SUPPRESS,
    )
