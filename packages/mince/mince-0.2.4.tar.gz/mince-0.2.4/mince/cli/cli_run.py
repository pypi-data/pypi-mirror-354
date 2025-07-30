from __future__ import annotations

import typing

import mince
from mince import Dashboard
from . import cli_parsing
from . import cli_helpers

if typing.TYPE_CHECKING:
    import argparse


def run_entire_cli() -> None:
    subcommands = [
        'ls',
        'cd',
        'dir',
        'register',
        'unregister',
        'validate',
        'collect',
        'run',
        'kill',
        'data',
        'spec',
        'docker',
    ]

    args = cli_parsing.parse_args(
        subcommands=subcommands,
        include_dashboard_arg=True,
        DashboardClass=None,
    )

    _execute(args, None)


def run_single_dashboard_cli(DashboardClass: type[Dashboard]) -> None:
    subcommands = [
        'cd',
        'dir',
        'register',
        'unregister',
        'validate',
        'collect',
        'run',
        'kill',
        'data',
        'spec',
    ]

    args = cli_parsing.parse_args(
        subcommands=subcommands,
        include_dashboard_arg=False,
        DashboardClass=DashboardClass,
    )

    _execute(args, DashboardClass)


def _execute(
    args: argparse.Namespace, DashboardClass: type[Dashboard] | None
) -> None:
    import inspect

    if args.pdb:
        try:
            if inspect.iscoroutinefunction(args.f_command):
                import asyncio

                asyncio.run(args.f_command(args, DashboardClass))
            else:
                args.f_command(args, DashboardClass)
        except Exception:
            cli_helpers._enter_debugger()
    else:
        if inspect.iscoroutinefunction(args.f_command):
            import asyncio

            asyncio.run(args.f_command(args, DashboardClass))
        else:
            args.f_command(args, DashboardClass)
