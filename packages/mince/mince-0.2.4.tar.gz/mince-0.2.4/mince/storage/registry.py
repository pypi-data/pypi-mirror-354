from __future__ import annotations

import os
import typing

from mince import dashboards

if typing.TYPE_CHECKING:
    from typing import Type, TypeVar
    from typing_extensions import TypeGuard
    from mince.types import (
        Registry,
        RegistryReference,
        RegistryEntry,
        CollectKwargsPartial,
    )

    T = TypeVar('T', bound=dashboards.Dashboard)


#
# # data loading
#


def get_registry_entry(
    name: str, registry: RegistryReference = None
) -> RegistryEntry:
    """load entry from registry"""
    registry = resolve_registry(registry)
    return registry['dashboards'][name]


#
# # reference resolution
#


def resolve_registry(registry: RegistryReference = None) -> Registry:
    """return Registry when reference is given as path or default (None)"""
    if isinstance(registry, str):
        registry = {'path': registry}
    if registry is None:
        return load_registry_file()
    elif isinstance(registry, dict) and 'path' in registry:
        return load_registry_file(
            path=registry.get('path'),  # type: ignore
            validate=registry.get('validate', True),  # type: ignore
            create_if_dne=registry.get('create_if_dne', True),  # type: ignore
        )
    elif isinstance(registry, dict) and 'dashboards' in registry:
        return registry  # type: ignore
    else:
        raise Exception('invalid registry reference')


#
# # registration
#


def register_dashboard(
    dashboard: str | Type[dashboards.Dashboard],
    *,
    registry: RegistryReference | None = None,
    collect_kwargs: CollectKwargsPartial | None = None,
) -> None:
    # resolve Dashboard class
    if isinstance(dashboard, str):
        if '.' in dashboard:
            DashboardClass = dashboards.resolve_dashboard_class(dashboard)
            dashboard_reference = dashboard
        else:
            DashboardClass = dashboards.find_dashboard_class(dashboard)
            dashboard_reference = (
                DashboardClass.__module__ + '.' + DashboardClass.__name__
            )
    elif issubclass(dashboard, dashboards.Dashboard):
        DashboardClass = dashboard
        dashboard_reference = (
            DashboardClass.__module__ + '.' + DashboardClass.__name__
        )
    else:
        raise Exception('dashboard class is not a subclass of Dashboard')

    # get metadata
    spec = DashboardClass.load_spec()
    name = spec['name']
    description = spec['description']
    if collect_kwargs is None:
        collect_kwargs = {}

    # add entry to registry
    entry: RegistryEntry = {
        'name': name,
        'dashboard_class': dashboard_reference,
        'description': description,
        'collect_kwargs': collect_kwargs,
    }
    resolved = resolve_registry(registry)
    resolved['dashboards'][name] = entry

    # save registry to disk
    if registry is None:
        save_registry_file(resolved, path=None)
    elif 'path' in registry:
        save_registry_file(
            resolved,
            path=registry['path'],  # type: ignore
        )

    print('registered', name)


def unregister_dashboard(
    name: str | typing.Type[dashboards.Dashboard],
    *,
    idempotent: bool = False,
    path: str | None = None,
    validate: bool = True,
) -> None:
    registry = load_registry_file(path=path, validate=validate)
    if isinstance(name, str):
        if name not in registry['dashboards'] and not idempotent:
            raise Exception('dashboard is not registered')
        del registry['dashboards'][name]
    elif type(name) is type and issubclass(name, dashboards.Dashboard):
        dashboard_path = name.__module__ + '.' + name.__name__
        for candidate_name, candidate in registry['dashboards'].items():
            if candidate['dashboard_class'] == dashboard_path:
                del registry['dashboards'][candidate_name]
    else:
        raise Exception('invalid type: ' + str(name))
    save_registry_file(registry=registry, path=path)


#
# # file io
#


def create_blank_registry() -> Registry:
    import mince

    return {
        'mince_version': mince.__version__,
        'dashboards': {},
    }


def load_registry_file(
    *,
    path: str | None = None,
    validate: bool = True,
    create_if_dne: bool = True,
) -> Registry:
    import json
    from mince import storage

    if path is None:
        path = storage.get_registry_path()
    if not os.path.exists(path):
        if create_if_dne:
            registry = create_blank_registry()
            save_registry_file(registry, path=path)
        else:
            raise Exception('registry file does not exist')
    else:
        with open(path, 'r') as f:
            registry = json.load(f)
    if validate_registry(registry):
        return registry
    else:
        raise Exception('invalid registry')


def save_registry_file(registry: Registry, *, path: str | None) -> None:
    import json
    from mince import storage

    if path is None:
        path = storage.get_registry_path()

    validate_registry(registry)

    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        json.dump(registry, f)


#
# # validation
#


def validate_registry(registry: typing.Any) -> TypeGuard[Registry]:
    if not isinstance(registry, dict):
        raise Exception('invalid type for registry: ' + str(type(registry)))
    assert set(registry.keys()) == {'mince_version', 'dashboards'}
    assert isinstance(registry['mince_version'], str)
    assert isinstance(registry['dashboards'], dict)
    for key, value in registry['dashboards'].items():
        assert isinstance(key, str)
        validate_registry_entry(value)
    return True


def validate_registry_entry(entry: typing.Any) -> TypeGuard[RegistryEntry]:
    assert isinstance(entry, dict)
    assert set(entry.keys()) == {
        'name',
        'dashboard_class',
        'description',
        'collect_kwargs',
    }
    assert isinstance(entry['name'], str)
    assert isinstance(entry['dashboard_class'], str)
    assert entry['description'] is None or isinstance(entry['description'], str)
    assert isinstance(entry['collect_kwargs'], dict)
    return True
