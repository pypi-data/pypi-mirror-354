from __future__ import annotations

import argparse
import typing

import mince.storage
from .. import cli_helpers
from .. import cli_parsing

if typing.TYPE_CHECKING:
    from mince import types


shell_snippet = """function mince {
    local tempfile="$(mktemp -t tmp.XXXXXX)"
    if [[ -z "$@" ]]; then
        command mince
    else
        command mince "$@" --cd-destination-tempfile "$tempfile"
    fi
    if [[ -s "$tempfile" ]]; then
        cd "$(realpath $(cat "$tempfile"))"
    fi
    rm -f "$tempfile" 2>/dev/null
}"""


def add_cd_command(
    subparsers: cli_helpers.Subparsers,
    include_dashboard_arg: bool,
    DashboardClass: typing.Type[mince.Dashboard] | None,
) -> None:
    parser = subparsers.add_parser(
        'cd',
        help='cd to mince root or dashboard data directory',
        formatter_class=cli_helpers.HelpFormatter,
    )
    parser.set_defaults(f_command=cd_command)
    if include_dashboard_arg:
        parser.add_argument('dashboard', help='dashboard name', nargs='?')

    parser.add_argument(
        '--code', help='cd to code directory', action='store_true'
    )
    cli_parsing.add_common_args(parser)


def cd_command(
    args: argparse.Namespace,
    dashboard: str | typing.Type[types.Dashboard] | None = None,
) -> None:
    import os

    if args.cd_destination_tempfile is None:
        print(
            'to enable `mince cd`, add this to your shell config (e.g. ~/.bashrc):'
        )
        print()
        print(shell_snippet)
    else:
        path = get_path(args, dashboard)
        os.makedirs(path, exist_ok=True)
        with open(args.cd_destination_tempfile, 'w') as f:
            f.write(path)


def get_path(
    args: argparse.Namespace,
    dashboard: str | typing.Type[types.Dashboard] | None = None,
) -> str:
    import importlib
    import os

    registry: types.RegistryFile = {
        'path': args.registry,
        'validate': not args.no_validate,
    }
    if dashboard is None:
        dashboard = args.dashboard
    if isinstance(dashboard, str):
        DashboardClass = mince.dashboards.get_dashboard_class(
            dashboard, registry=registry
        )
    elif type(dashboard) is mince.Dashboard and issubclass(
        dashboard, mince.Dashboard
    ):
        DashboardClass = dashboard
    else:
        DashboardClass = None
    if DashboardClass is None:
        if args.code:
            return os.path.dirname(mince.__file__)
        else:
            return mince.storage.get_mince_root()
    else:
        if args.code:
            module = importlib.import_module(DashboardClass.__module__)
            return os.path.dirname(module.__file__)  # type: ignore
        else:
            return mince.storage.resolve_data_dir(
                dashboard=DashboardClass,
                registry=registry,
            )
