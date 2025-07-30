"""
Collection parameters come from 3 places (in this order of precedence):
1. arguments passed directly to collect_dashboard_data()
2. arguments stored in the dashboard registry
3. arguments returned by DashboardClass.get_default_collect_kwargs()
"""

from __future__ import annotations

import typing

from mince import dashboards
from mince import schemas
from mince import specs
from mince import storage

if typing.TYPE_CHECKING:
    from typing import Type

    T = typing.TypeVar('T')
    import polars as pl
    import tooltime
    from mince import types


async def async_collect_dashboard_data(
    dashboard: str | Type[dashboards.Dashboard],
    *,
    registry: types.RegistryReference = None,
    data_dir: str | None = None,
    start_time: tooltime.Timestamp | None = None,
    end_time: tooltime.Timestamp | None = None,
    intervals: list[types.Interval] | None = None,
    skip_incomplete_intervals: bool | None = None,
    extra_kwargs: dict[str, typing.Any] | None = None,
    extra_kwargs_update: dict[str, typing.Any] | None = None,
    dry: bool | None = None,
    verbose: int | None = None,
) -> dict[str, pl.DataFrame]:
    import time
    import tooltime

    # gather metadata
    # (must gather before collection because want pre-start git commit versions)
    job_start_time = time.time()
    mince_version = specs.get_package_version('mince')

    # get dashboard class
    (
        dashboard_class,
        dashboard_name,
        dashboard_version,
        registry_entry,
    ) = _resolve_dashboard(dashboard=dashboard, registry=registry)

    # gather collect kwargs
    collect_kwargs = _resolve_collect_kwargs(
        dashboard_name=dashboard_name,
        dashboard_class=dashboard_class,
        class_collect_kwargs=dashboard_class.get_default_collect_kwargs(),
        registry_entry=registry_entry,
        direct_collect_kwargs=dict(
            data_dir=data_dir,
            start_time=start_time,
            end_time=end_time,
            intervals=intervals,
            skip_incomplete_intervals=skip_incomplete_intervals,
            extra_kwargs=extra_kwargs,
            extra_kwargs_update=extra_kwargs_update,
            dry=dry,
            verbose=verbose,
        ),
    )

    # print summary
    if collect_kwargs['verbose'] >= 1:
        _print_collection_summary(
            dashboard_class=dashboard_class,
            dashboard_name=dashboard_name,
            dashboard_version=dashboard_version,
            mince_version=mince_version,
            collect_kwargs=collect_kwargs,
            job_start_time=job_start_time,
        )

    # collect data
    dfs = await dashboard_class.async_collect_data(**collect_kwargs)
    job_end_time = time.time()

    # validate data
    spec = dashboard_class.load_spec()
    schemas.validate_data_matches_spec(dfs, spec)

    # create job metadata
    job: types.CollectionJobSummary = {
        'mince_version': mince_version,
        'dashboard_version': dashboard_version,
        'dashboard_name': dashboard_name,
        'dashboard_class': (
            dashboard_class.__module__ + '.' + dashboard_class.__name__
        ),
        'job_start_time': job_start_time,
        'job_end_time': job_end_time,
        'data_names': list(dfs.keys()),
        'collect_kwargs': collect_kwargs,
    }

    # write results
    if not dry:
        storage.write_job_results(job=job, dfs=dfs)

    # print summary
    if collect_kwargs['verbose'] >= 1:
        print()
        duration = '%.02f' % (job_end_time - job_start_time)
        print(
            'collection completed in',
            duration,
            'seconds at',
            tooltime.timestamp_to_iso_pretty(job_end_time),
        )

    return dfs


def _print_collection_summary(
    *,
    dashboard_class: Type[types.Dashboard],
    dashboard_name: str,
    dashboard_version: str,
    mince_version: str,
    collect_kwargs: types.CollectKwargs,
    job_start_time: tooltime.Timestamp,
) -> None:
    import toolstr
    import tooltime

    toolstr.print_text_box('collecting data')
    print()
    toolstr.print_header('Dashboard')
    print('- name:', dashboard_name)
    print(
        '- class:', dashboard_class.__module__ + '.' + dashboard_class.__name__
    )
    print('- dashboard version:', dashboard_version)
    print('- mince version:', mince_version)
    print()
    toolstr.print_header('Collection')
    for key, value in collect_kwargs.items():
        if key in ['start_time', 'end_time']:
            print('-', key + ':', tooltime.timestamp_to_iso_pretty(value))  # type: ignore
        elif isinstance(value, dict):
            print('-', key + ':')
            for subkey, subvalue in value.items():
                print('    -', subkey + ':', subvalue)
        else:
            print('-', key + ':', value)
    print('- job start time:', tooltime.timestamp_to_iso_pretty(job_start_time))


def _validate_data(
    dfs: typing.Any,
    DashboardClass: typing.Type[types.Dashboard],
) -> None:
    import polars as pl

    # check type
    if (not isinstance(dfs, dict)) or any(
        not isinstance(name, str) or not isinstance(df, pl.DataFrame)
        for name, df in dfs.items()
    ):
        raise Exception('invalid format for data')


def _resolve_dashboard(
    dashboard: str | Type[dashboards.Dashboard],
    registry: types.RegistryReference = None,
) -> tuple[Type[types.Dashboard], str, str, types.RegistryEntry | None]:
    if isinstance(dashboard, str):
        dashboard_class = dashboards.get_dashboard_class(
            dashboard, registry=registry
        )
        dashboard_name = dashboard
        entry = storage.get_registry_entry(dashboard, registry=registry)
    elif type(dashboard) is type and issubclass(
        dashboard, dashboards.Dashboard
    ):
        dashboard_class = dashboard
        dashboard_name = None
        entry = None
    else:
        raise Exception('invalid format for dashboard')

    spec = dashboard_class.load_spec()
    if dashboard_name is None:
        dashboard_name = spec['name']
    version = spec['version']

    return dashboard_class, dashboard_name, version, entry


def _resolve_collect_kwargs(
    dashboard_name: str,
    dashboard_class: Type[dashboards.Dashboard],
    class_collect_kwargs: types.CollectKwargsPartial,
    registry_entry: types.RegistryEntry | None,
    direct_collect_kwargs: types.CollectKwargsPartial,
) -> types.CollectKwargs:
    import tooltime

    # gather all kwargs sets
    if registry_entry is not None:
        registry_collect_kwargs = registry_entry['collect_kwargs']
    else:
        registry_collect_kwargs = {}
    all_kwargs = [
        direct_collect_kwargs,
        registry_collect_kwargs,
        class_collect_kwargs,
    ]

    # data_dir
    data_dir = first_non_none([kwargs.get('data_dir') for kwargs in all_kwargs])
    if data_dir is None:
        data_dir = storage.get_dashboard_data_dir(dashboard_name)

    # start_time
    raw_start_time = first_non_none(  # type: ignore
        [kwargs.get('start_time') for kwargs in all_kwargs]
    )
    if raw_start_time is None:
        raise Exception('raw_start_time not specified')
    start_time = tooltime.timestamp_to_seconds_precise(raw_start_time)

    # end_time
    raw_end_time = first_non_none(  # type: ignore
        [kwargs.get('end_time') for kwargs in all_kwargs]
    )
    if raw_end_time is None:
        raise Exception('raw_end_time not specified')
    end_time = tooltime.timestamp_to_seconds_precise(raw_end_time)

    # intervals
    intervals = first_non_none(
        [kwargs.get('intervals') for kwargs in all_kwargs]
    )
    if intervals is None:
        raise Exception('intervals not specified')

    # skip_incomplete_intervals
    skip_incomplete_intervals = first_non_none(
        [kwargs.get('skip_incomplete_intervals') for kwargs in all_kwargs]
    )
    if skip_incomplete_intervals is None:
        raise Exception('skip_incomplete_intervals not specified')

    # extra_kwargs
    extra_kwargs = first_non_none(
        [kwargs.get('extra_kwargs') for kwargs in all_kwargs]
    )
    if extra_kwargs is None:
        raise Exception('extra_kwargs not specified')
    extra_kwargs = extra_kwargs.copy()

    # extra kwargs update
    for kwargs in all_kwargs:
        extra_kwargs_update = kwargs.get('extra_kwargs_update')
        if extra_kwargs_update is not None:
            for key, value in extra_kwargs_update.items():
                if extra_kwargs.get(key) is None:
                    extra_kwargs[key] = value

    # dry
    dry = first_non_none([kwargs.get('dry') for kwargs in all_kwargs])
    if dry is None:
        raise Exception('dry not specified')

    # verbose
    verbose = first_non_none([kwargs.get('verbose') for kwargs in all_kwargs])
    if verbose is None:
        raise Exception('verbose not specified')

    return {
        'data_dir': data_dir,
        'start_time': start_time,
        'end_time': end_time,
        'intervals': intervals,
        'skip_incomplete_intervals': skip_incomplete_intervals,
        'extra_kwargs': extra_kwargs,
        'dry': dry,
        'verbose': verbose,
    }


def first_non_none(lst: list[T | None]) -> T | None:
    return next((x for x in lst if x is not None), None)
