from __future__ import annotations

import typing

if typing.TYPE_CHECKING:
    from mince import types


def parse_url(
    url_search: str,
    display: dict[str, str],
    defaults: dict[str, types.StateDatum | None],
) -> None:
    import urllib.parse

    parsed = urllib.parse.parse_qs(urllib.parse.urlparse(url_search).query)
    for key in defaults.keys():
        if key in parsed:
            display[key] = parsed[key][0]
    if 'now' in parsed:
        display['now'] = parsed['now'][0]


def create_new_url(
    display: dict[str, str],
    defaults: dict[str, types.StateDatum | None],
) -> str:
    params: list[str] = []
    for key, value in defaults.items():
        if display[key] != str(value):
            params.append(key + '=' + display[key])

    return '?' + '&'.join(params) if params else ''
