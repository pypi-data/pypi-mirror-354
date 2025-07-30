from __future__ import annotations

import argparse
import typing

import mince
from ... import ops
from .. import cli_helpers
from .. import cli_parsing

if typing.TYPE_CHECKING:
    from mince import types


def add_collect_command(
    subparsers: cli_helpers.Subparsers,
    include_dashboard_arg: bool,
    DashboardClass: typing.Type[types.Dashboard] | None,
) -> None:
    parser = subparsers.add_parser(
        'collect',
        help='collect data of dashboard',
        formatter_class=cli_helpers.HelpFormatter,
        allow_abbrev=False,
    )
    if include_dashboard_arg:
        parser.add_argument('dashboard', help='dashboard to collect data of')
    parser.add_argument('--data-dir', help='data directory')
    parser.add_argument(
        '--start', help='start date to use [default = ETH_GENESIS]'
    )
    parser.add_argument(
        '--end',
        help='end date to use [default = now]',
    )
    parser.add_argument(
        '--intervals',
        nargs='+',
        metavar='INTERVAL',
        help='intervals to collect: {day week month}',
    )
    parser.add_argument(
        '--skip-incomplete-intervals',
        help='skip incomplete time intervals instead of collecting them',
        action='store_true',
    )
    parser.add_argument(
        '--extra-kwargs', metavar='JSON', help='raw extra kwargs, as json'
    )
    parser.add_argument(
        '--extra-kwargs-update',
        metavar='JSON',
        help='raw extra kwargs update, as json',
    )
    parser.add_argument('--dry', help='dry run', action='store_true')
    parser.add_argument(
        '--verbose',
        help='verbosity level',
        nargs='?',
        default=None,
        type=int,
        const=1,
    )

    if DashboardClass is not None:
        custom_args = get_custom_cli_args(DashboardClass)
        for name, spec in custom_args.items():
            parser.add_argument(*name, **spec)

    parser.set_defaults(f_command=collect_command)
    cli_parsing.add_common_args(parser)


async def collect_command(
    args: argparse.Namespace,
    dashboard: str | typing.Type[types.Dashboard] | None = None,
) -> None:
    # parse registry
    registry: types.RegistryFile = {
        'path': args.registry,
        'validate': not args.no_validate,
    }

    # parse dashboard class
    if dashboard is None:
        dashboard = args.dashboard
    if isinstance(dashboard, str):
        DashboardClass = mince.dashboards.get_dashboard_class(
            name=dashboard, registry=registry
        )
    elif type(dashboard) is type and issubclass(dashboard, mince.Dashboard):
        DashboardClass = dashboard
    else:
        raise Exception()

    # collect input CollectKwargs
    input_collect_kwargs = get_input_collect_kwargs(args, DashboardClass)

    # parse custom extra_kwargs arguments
    collect_kwargs = ops.collection.collection_run._resolve_collect_kwargs(
        dashboard_name=DashboardClass.load_spec()['name'],
        dashboard_class=DashboardClass,
        class_collect_kwargs=DashboardClass.get_default_collect_kwargs(),
        direct_collect_kwargs=input_collect_kwargs,
        registry_entry=None,  # TODO: include registry entry
    )

    await ops.async_collect_dashboard_data(
        dashboard=dashboard,
        registry=registry,
        **collect_kwargs,
    )


def get_custom_cli_args(
    DashboardClass: type[mince.Dashboard],
) -> dict[tuple[str], dict[str, typing.Any]]:
    collect_kwargs = ops.collection.collection_run._resolve_collect_kwargs(
        dashboard_name=DashboardClass.load_spec()['name'],
        dashboard_class=DashboardClass,
        class_collect_kwargs=DashboardClass.get_default_collect_kwargs(),
        direct_collect_kwargs={},
        registry_entry=None,  # TODO: include registry entry
    )
    args = {}
    for key, value in collect_kwargs['extra_kwargs'].items():
        name = '--' + key.replace('_', '-')
        help_str = key.replace('_', ' ') + ' collection parameter'
        metavar = 'VALUE'
        if isinstance(value, bool):
            if value:
                name = name.replace('--', '--no-')
            spec = dict(
                help=help_str,
                action='store_const',
                const=True,
                default=None,
            )
        elif isinstance(value, (str, int, float)):
            spec = dict(help=help_str, metavar=metavar, type=type(value))
        elif isinstance(value, list):
            spec = dict(help=help_str, metavar=metavar, nargs='*')
        else:
            raise Exception('invalid extra_args type for cli: ' + str())
        args[(name,)] = spec
    return args


def get_input_collect_kwargs(
    args: argparse.Namespace,
    DashboardClass: type[mince.Dashboard],
) -> mince.CollectKwargsPartial:
    import json

    # parse extra_kwargs
    if args.extra_kwargs is not None:
        extra_kwargs = json.loads(args.extra_kwargs)
    else:
        extra_kwargs = None
    if args.extra_kwargs_update is not None:
        extra_kwargs_update = json.loads(args.extra_kwargs_update)
    else:
        extra_kwargs_update = {}

    custom_cli_args = get_custom_cli_args(DashboardClass)
    for names, spec in custom_cli_args.items():
        input_name = names[-1].lstrip('-').replace('-', '_')
        if input_name.startswith('no_'):
            extra_kwargs_update[input_name[3:]] = not getattr(args, input_name)
        else:
            extra_kwargs_update[input_name] = getattr(args, input_name)

    return {
        'data_dir': args.data_dir,
        'start_time': args.start,
        'end_time': args.end,
        'intervals': args.intervals,
        'skip_incomplete_intervals': args.skip_incomplete_intervals,
        'extra_kwargs': extra_kwargs,
        'extra_kwargs_update': extra_kwargs_update,
        'dry': args.dry,
        'verbose': args.verbose,
    }
