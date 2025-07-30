"""perform dashboard management actions"""

from __future__ import annotations

import typing

import mince.dashboards

if typing.TYPE_CHECKING:
    from typing import Type
    from mince import types


def run_dashboard(
    dashboard: str | Type[mince.dashboards.Dashboard],
    *,
    instance_kwargs: typing.Mapping[str, typing.Any] | None = None,
    run_kwargs: typing.Mapping[str, typing.Any] | None = None,
    registry: types.RegistryReference = None,
) -> None:
    instance = mince.dashboards.instantiate_dashboard(
        dashboard=dashboard,
        registry=registry,
        instance_kwargs=instance_kwargs,
    )

    # run dashboard
    if run_kwargs is None:
        run_kwargs = {}
    instance.run(**run_kwargs)


def find_available_port(
    min_port: int | str = 8052, *, n_attempts: int = 100
) -> int:
    import socket

    port = int(min_port)
    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('localhost', port))
                return port
        except OSError:
            port += 1
