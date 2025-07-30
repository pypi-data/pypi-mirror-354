from __future__ import annotations

import typing

from mince import storage
from .dashboard_class import Dashboard

if typing.TYPE_CHECKING:
    from typing import Type
    from mince import types


def get_dashboard_class(
    name: str, *, registry: types.RegistryReference = None
) -> Type[Dashboard]:
    """syntax:

    module.submodule.DashboardClass
    OR
    registered_name
    """
    if '.' in name:
        return resolve_dashboard_class(name)
    else:
        entry = storage.get_registry_entry(name=name, registry=registry)
        return resolve_dashboard_class(entry['dashboard_class'])


def resolve_dashboard_class(reference: str) -> Type[Dashboard]:
    """syntax:

    module.submodule.DashboardClassName
    OR
    module (will try module.mince)
    """
    import importlib

    *module_name_pieces, class_name = reference.split('.')
    module_name = '.'.join(module_name_pieces)
    module = importlib.import_module(module_name)
    DashboardClass: type[Dashboard] = getattr(module, class_name)
    if not issubclass(DashboardClass, Dashboard):
        raise Exception('not a subclass of Dashboard')
    return DashboardClass


def find_dashboard_class(package: str) -> Type[Dashboard]:
    import importlib

    module_name = package + '.mince'
    module = importlib.import_module(module_name)
    candidates = []
    for name, value in vars(module).items():
        if type(value) is type and issubclass(value, Dashboard):
            candidates.append(value)
    if len(candidates) == 0:
        raise Exception('no Dashboard classes in ' + module_name)
    elif len(candidates) > 1:
        raise Exception('multiple Dashboard classes in ' + module_name)
    else:
        return candidates[0]


def instantiate_dashboard(
    dashboard: str | Type[Dashboard],
    *,
    registry: types.RegistryReference = None,
    instance_kwargs: typing.Mapping[str, typing.Any] | None = None,
) -> Dashboard:
    # load data
    data_dir = storage.resolve_data_dir(dashboard, registry=registry)
    job, dfs = storage.load_dashboard_data(data_dir=data_dir)

    # get dashboard class
    if isinstance(dashboard, str):
        DashboardClass = get_dashboard_class(dashboard, registry=registry)
    elif issubclass(dashboard, Dashboard):
        DashboardClass = dashboard
    else:
        raise Exception()

    # load spec
    ui_spec = DashboardClass.load_spec()

    # create dashboard instance
    date_range = (
        job['collect_kwargs']['start_time'],
        job['collect_kwargs']['end_time'],
    )
    if instance_kwargs is None:
        instance_kwargs = {}
    return DashboardClass(
        dfs=dfs, spec=ui_spec, job=job, date_range=date_range, **instance_kwargs
    )
