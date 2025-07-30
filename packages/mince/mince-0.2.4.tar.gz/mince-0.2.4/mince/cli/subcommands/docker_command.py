from __future__ import annotations

import argparse
import typing

import mince
from .. import cli_helpers
from .. import cli_parsing


def add_docker_command(
    subparsers: cli_helpers.Subparsers,
    include_dashboard_arg: bool,
    DashboardClass: typing.Type[mince.Dashboard] | None,
) -> None:
    """
    mince docker build <dashboard> [--name name]
    """
    parser = subparsers.add_parser(
        'docker',
        help='performance docker',
        formatter_class=cli_helpers.HelpFormatter,
    )
    parser.set_defaults(f_command=docker_command)
    parser.add_argument('subcommand', help='docker command {build}')
    if include_dashboard_arg:
        parser.add_argument('dashboard', help='dashboard name')
    cli_parsing.add_common_args(parser)


def docker_command(args: argparse.Namespace) -> None:
    command = args.command
    dashboard = args.dashboard
    print('COMMAND', command)
    print('DASHBOARD', dashboard)

    if command == 'build':
        build_dashboard_docker_image()
    else:
        raise Exception()


def build_dashboard_docker_image() -> None:
    pass
