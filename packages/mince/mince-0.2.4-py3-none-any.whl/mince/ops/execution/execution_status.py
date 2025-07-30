from __future__ import annotations

import os
import typing

if typing.TYPE_CHECKING:
    from mince import Dashboard


pid_dir = '/tmp/mince/running'


def get_pid_path(*, dashboard: Dashboard, port: int | str, pid: int) -> str:
    pid_template = os.path.join(pid_dir, '{dashboard}__port_{port}__pid_{pid}')
    return pid_template.format(
        dashboard=dashboard.spec['name'],
        port=port,
        pid=pid,
    )


def create_pid_file(dashboard: Dashboard, port: str) -> None:
    pid = os.getpid()
    path = get_pid_path(dashboard=dashboard, port=port, pid=pid)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as _:
        pass


def clear_pid_file(dashboard: Dashboard, port: str) -> None:
    pid = os.getpid()
    path = get_pid_path(dashboard=dashboard, port=port, pid=pid)
    try:
        os.remove(path)
    except OSError:
        pass


def get_running_servers() -> list[dict[str, typing.Any]]:
    servers = []
    for filename in os.listdir(pid_dir):
        # parse pid filename
        pieces = filename.split('__')
        server: dict[str, typing.Any] = {
            'name': pieces[0],
            'port': pieces[1].split('_')[1],
            'pid': pieces[2].split('_')[1],
        }

        # get server metadata
        try:
            server['metadata'] = get_server_metadata(server)
        except Exception:
            os.remove(os.path.join(pid_dir, filename))
            continue

        servers.append(server)

    return servers


def get_server_metadata(server: dict[str, typing.Any]) -> dict[str, typing.Any]:
    import requests

    url = 'http://localhost:' + str(server['port']) + '/metadata'
    response = requests.get(url)
    return response.json()  # type: ignore


def kill_server(
    *,
    name: str | None = None,
    pid: str | int | None = None,
    port: str | int | None = None,
) -> None:
    import signal

    if pid is not None:
        pid = str(pid)
    if port is not None:
        port = str(port)

    if name is None and pid is None and port is None:
        raise Exception('must specify name or pid or port')

    candidates = []
    for server in get_running_servers():
        if name is not None and name != server['name']:
            continue
        if port is not None and port != server['port']:
            continue
        if pid is not None and pid != server['pid']:
            continue
        candidates.append(server)

    if len(candidates) == 0:
        print('[no matching dashboards]')
    elif len(candidates) == 1:
        print('killing 1 dashboard')
    else:
        print('killing', len(candidates), 'dashboards')

    for server in candidates:
        os.kill(int(server['pid']), signal.SIGTERM)
