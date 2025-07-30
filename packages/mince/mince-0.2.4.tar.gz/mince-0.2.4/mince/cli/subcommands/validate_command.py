from __future__ import annotations

import argparse
import typing

import mince
from ... import dashboards
from ... import storage
from .. import cli_helpers
from .. import cli_parsing

if typing.TYPE_CHECKING:
    from mince import types


def add_validate_command(
    subparsers: cli_helpers.Subparsers,
    include_dashboard_arg: bool,
    DashboardClass: typing.Type[mince.Dashboard] | None,
) -> None:
    parser = subparsers.add_parser(
        'validate',
        help='validate dashboard spec and data',
        formatter_class=cli_helpers.HelpFormatter,
    )
    parser.set_defaults(f_command=validate_command)
    if include_dashboard_arg:
        parser.add_argument(
            'dashboard',
            help='dashboard to validate',
            nargs='?',
        )
    parser.add_argument(
        '--spec',
        help='validate spec specifically',
        action='store_true',
    )
    parser.add_argument(
        '--data',
        help='validate data specifically',
        action='store_true',
    )
    parser.add_argument(
        '--registry',
        help='validate registry specifically',
        action='store_true',
    )
    cli_parsing.add_common_args(parser, registry_name='--registry-path')


def validate_command(
    args: argparse.Namespace,
    dashboard: str | typing.Type[types.Dashboard] | None = None,
) -> None:
    # determine validation targets
    if not args.registry and not args.spec and not args.data:
        targets = ['registry', 'spec', 'data']
    else:
        targets = []
        if args.registry:
            targets.append('registry')
        if args.spec:
            targets.append('spec')
        if args.data:
            targets.append('data')

    # validate registry
    if 'registry' in targets:
        storage.resolve_registry(args.registry_path)

    # validate each dashboard
    if args.dashboard is None and dashboard is None:
        # validate all dashboards
        registry = storage.resolve_registry(args.registry_path)
        names = list(registry['dashboards'].keys())
        if len(registry['dashboards']) == 0:
            print('[no registered dashboards]')
        elif len(registry['dashboards']) > 2:
            print('validating', len(names), 'dashboards:', ', '.join(names))
        for name, entry in registry['dashboards'].items():
            validate_dashboard(
                name=entry['name'],
                dashboard=entry['dashboard_class'],
                targets=targets,
                registry=args.registry_path,
            )
    elif dashboard is not None:
        if type(dashboard) is type and issubclass(dashboard, types.Dashboard):
            validate_dashboard(
                name=dashboard.__name__,
                dashboard=dashboard,
                targets=targets,
                registry=args.registry_path,
            )
        elif isinstance(dashboard, str):
            validate_dashboard(
                name=dashboard,
                targets=targets,
                registry=args.registry_path,
            )
        else:
            raise Exception(
                'invalid type for dashboard: ' + str(type(dashboard))
            )
    else:
        validate_dashboard(
            name=args.dashboard,
            targets=targets,
            registry=args.registry_path,
        )


def validate_dashboard(
    name: str,
    *,
    dashboard: str | typing.Type[types.Dashboard] | None = None,
    targets: list[str],
    registry: str | None,
) -> None:
    import mince.schemas
    import mince.types

    print('validating', dashboard)

    if dashboard is not None:
        if isinstance(dashboard, str):
            DashboardClass = dashboards.get_dashboard_class(
                dashboard, registry=registry
            )
        elif type(dashboard) is type and issubclass(dashboard, types.Dashboard):
            DashboardClass = dashboard
        else:
            raise Exception('invalid type for dashboard')
    else:
        DashboardClass = dashboards.get_dashboard_class(name, registry=registry)

    if 'spec' in targets or 'data' in targets:
        spec = DashboardClass.load_spec()
    if 'spec' in targets:
        mince.types.validate_typeddict(spec, mince.types.UiSpec)
        print('    validated', name, 'spec')
    if 'data' in targets:
        if dashboard is not None:
            data_dir = storage.resolve_data_dir(dashboard)
        else:
            data_dir = storage.resolve_data_dir(name)
        job, dfs = storage.load_dashboard_data(data_dir=data_dir)
        mince.schemas.validate_data_matches_spec(dfs=dfs, spec=spec)
        print('    validated', name, 'data')
