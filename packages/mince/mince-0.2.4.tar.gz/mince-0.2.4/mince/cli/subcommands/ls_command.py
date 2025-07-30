from __future__ import annotations

import argparse
import typing

import mince.ops
from ... import storage
from .. import cli_helpers
from .. import cli_parsing

if typing.TYPE_CHECKING:
    from mince import types


def add_ls_command(
    subparsers: cli_helpers.Subparsers,
    include_dashboard_arg: bool,
    DashboardClass: typing.Type[mince.Dashboard] | None,
) -> None:
    parser = subparsers.add_parser(
        'ls',
        help='list registered or running dashboards',
        formatter_class=cli_helpers.HelpFormatter,
    )
    parser.set_defaults(f_command=ls_command)
    parser.add_argument(
        '-v',
        '--verbose',
        help='print extra info',
        action='store_true',
    )
    parser.add_argument(
        '--raw',
        help='print all info as raw json',
        action='store_true',
    )
    cli_parsing.add_common_args(parser)


def ls_command(args: argparse.Namespace, DashboardClass: typing.Any) -> None:
    print_registered_dashboards(args)
    print()
    print()
    print_running_dashboards(args)


def print_registered_dashboards(
    args: argparse.Namespace,
    dashboard: str | typing.Type[types.Dashboard] | None = None,
) -> None:
    import toolstr
    import rich

    rich.print('[bold][white]Registered dashboards:[/white][/bold]')
    registry = storage.load_registry_file(
        path=args.registry,
        validate=not args.no_validate,
    )
    if len(registry['dashboards']) == 0:
        print('[none]')
    else:
        if args.raw:
            import json

            print(json.dumps(list(registry.values()), indent=4, sort_keys=True))
            return
        rows = []
        for entry in registry['dashboards'].values():
            description = entry['description']
            row = [entry['name'], description]
            if args.verbose:
                row.append(entry['dashboard_class'])
            rows.append(row)
        labels = ['name', 'description']
        if args.verbose:
            labels.append('class')
        print()
        toolstr.print_table(
            rows,
            labels=labels,
            border='rgb(100,100,100)',
            column_styles={'name': 'green'},
            label_style='bold white',
            outer_gap=0,
            label_justify='left',
            column_justify='left',
        )


def print_running_dashboards(args: argparse.Namespace) -> None:
    import toolstr
    import tooltime
    import rich

    servers = mince.ops.get_running_servers()
    rich.print('[bold][white]Running dashboards:[/white][/bold]')
    if len(servers) == 0:
        print('[no running dashboards]')
    else:
        if args.raw:
            import json

            print(json.dumps(list(servers), indent=4, sort_keys=True))
            return
        print()
        rows = []
        for server in servers:
            row = [
                server['name'],
                'localhost:' + server['port'],
                'd = '
                + server['metadata']['dashboard_version']
                + '\n'
                + 'm = '
                + server['metadata']['mince_version'],
                server['metadata']['time_started'].replace(' ', '\n'),
                tooltime.timelength_to_clock_phrase(
                    float(tooltime.now())  # type: ignore
                    - tooltime.timestamp_to_seconds(
                        server['metadata']['time_started']
                    )
                ),
            ]
            if args.verbose:
                row.append(server['pid'])
            rows.append(row)

        labels = [
            'name',
            'url',
            'versions',
            'time\nstarted',
            'uptime',
        ]
        if args.verbose:
            labels.append('pid')
        toolstr.print_multiline_table(
            rows,
            labels=labels,
            border='rgb(100,100,100)',
            column_styles={'name': 'green'},
            label_style='bold white',
            column_justify='left',
            label_justify='left',
            outer_gap=0,
        )
