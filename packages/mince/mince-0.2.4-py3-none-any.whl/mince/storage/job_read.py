from __future__ import annotations

import os
import typing

from . import paths

if typing.TYPE_CHECKING:
    from mince import types
    import polars as pl


def load_dashboard_data(
    *,
    data_dir: str | None = None,
    dashboard: str | None = None,
    job_start_time: int | None = None,
) -> tuple[types.CollectionJobSummary, dict[str, pl.DataFrame]]:
    import polars as pl

    # load job
    if job_start_time is None:
        job = read_latest_job_summary(dashboard=dashboard, data_dir=data_dir)
        if job is None:
            raise Exception('no collection jobs have been run')
    else:
        job = read_job_summary(
            dashboard=dashboard, data_dir=data_dir, timestamp=job_start_time
        )

    # load data
    if data_dir is None:
        data_dir = paths.get_dashboard_data_dir(dashboard=job['dashboard_name'])
    dfs = {}
    for datum_name in job['data_names']:
        path = paths.get_job_datum_path(
            datum_name=datum_name,
            data_dir=data_dir,
            timestamp=job['job_start_time'],
        )
        dfs[datum_name] = pl.read_parquet(path)

    return job, dfs


def read_job_summary(
    *,
    dashboard: str | None = None,
    data_dir: str | None = None,
    timestamp: int | None = None,
) -> types.CollectionJobSummary:
    raise Exception()


def read_latest_job_summary(
    *,
    dashboard: str | None = None,
    data_dir: str | None = None,
) -> types.CollectionJobSummary | None:
    import json

    # get path
    latest_path = paths.get_job_latest_path(
        dashboard=dashboard, data_dir=data_dir
    )

    # load data
    if not os.path.isfile(latest_path):
        return None
    else:
        with open(latest_path, 'r') as f:
            job: types.CollectionJobSummary = json.load(f)
            return job
