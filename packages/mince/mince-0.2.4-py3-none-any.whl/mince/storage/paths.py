"""
path layout is identical on local filesystem vs http server

Layout:
- {root_dir}/{dashboard}/
    - fragments/
    - latest.json --> symlink to a data.json
    - jobs
        - 2024-01-05/
            - data.json
            - datum1.parquet
            - datum2.parquet
            - datum3.parquet
        - 2024-01-04/
            - data.json
            - datum1.parquet
            - datum2.parquet
            - datum3.parquet
        - 2024-01-03/
            - data.json
            - datum1.parquet
            - datum2.parquet
            - datum3.parquet
"""

from __future__ import annotations

import os
import typing

from . import registry as registry_module

if typing.TYPE_CHECKING:
    from mince import types


def get_mince_root() -> str:
    path = os.environ.get('MINCE_ROOT')
    if path is None:
        print('MINCE_ROOT not set, using ~/mince as default mince root')
        path = '~/data/mince'
    return os.path.expanduser(path)


def get_registry_path() -> str:
    path = os.environ.get('MINCE_REGISTRY_PATH')
    if path is None:
        path = os.path.join(get_mince_root(), 'mince_registry.json')
    return os.path.expanduser(path)


#
# # registry resolution
#


def resolve_data_dir(
    dashboard: str | typing.Type[types.Dashboard],
    registry: types.RegistryReference = None,
) -> str:
    """input is either a registry entry name or a Dashboard subclass"""
    import mince

    if isinstance(dashboard, str):
        registry_entry = registry_module.get_registry_entry(
            dashboard, registry=registry
        )
        registry_data_dir = registry_entry['collect_kwargs'].get('data_dir')
        if registry_data_dir is not None:
            return registry_data_dir
        else:
            return get_dashboard_data_dir(dashboard)
    elif type(dashboard) is type and issubclass(dashboard, mince.Dashboard):
        spec = dashboard.load_spec()
        return get_dashboard_data_dir(spec['name'])
    else:
        raise Exception('invalid type')


#
# # absolute paths
#


def get_dashboard_data_dir(dashboard: str | None) -> str:
    if dashboard is None:
        raise Exception('specify data_dir or dashboard')
    return os.path.join(get_mince_root(), dashboard)


def get_job_dir(
    *,
    timestamp: int | float,
    dashboard: str | None = None,
    data_dir: str | None = None,
) -> str:
    if data_dir is None:
        data_dir = get_dashboard_data_dir(dashboard=dashboard)
    return os.path.join(data_dir, get_job_reldir(timestamp=timestamp))


def get_job_metadata_path(
    *,
    timestamp: int | float,
    dashboard: str | None = None,
    data_dir: str | None = None,
) -> str:
    if data_dir is None:
        data_dir = get_dashboard_data_dir(dashboard=dashboard)
    return os.path.join(data_dir, get_job_metadata_relpath(timestamp=timestamp))


def get_job_datum_path(
    *,
    datum_name: str,
    timestamp: int | float,
    dashboard: str | None = None,
    data_dir: str | None = None,
) -> str:
    if data_dir is None:
        data_dir = get_dashboard_data_dir(dashboard=dashboard)
    relpath = get_job_datum_relpath(datum_name=datum_name, timestamp=timestamp)
    return os.path.join(data_dir, relpath)


def get_job_latest_path(
    *,
    dashboard: str | None = None,
    data_dir: str | None = None,
) -> str:
    if data_dir is None:
        data_dir = get_dashboard_data_dir(dashboard=dashboard)
    return os.path.join(data_dir, get_latest_job_relpath())


#
# # relative paths
#


def get_job_reldir(timestamp: int | float) -> str:
    import datetime

    dt = datetime.datetime.fromtimestamp(timestamp)
    dt_str = dt.strftime('%Y-%m-%d_%H-%M-%S.%f')
    return os.path.join('jobs', dt_str)


def get_job_metadata_relpath(timestamp: int | float) -> str:
    job_dir = get_job_reldir(timestamp=timestamp)
    return os.path.join(job_dir, 'data.json')


def get_job_datum_relpath(datum_name: str, timestamp: int | float) -> str:
    job_dir = get_job_reldir(timestamp=timestamp)
    return os.path.join(job_dir, datum_name + '.parquet')


def get_latest_job_relpath() -> str:
    return 'latest.json'
