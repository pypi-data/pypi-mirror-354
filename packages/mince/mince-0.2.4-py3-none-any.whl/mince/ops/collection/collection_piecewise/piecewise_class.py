from __future__ import annotations

import typing
import mince

if typing.TYPE_CHECKING:
    import polars as pl


class PiecewiseCollector:
    path_template: str
    tag_names: list[str]

    @classmethod
    def get_chunk_time_range(
        cls,
        start_time: int,
        end_time: int,
        interval: mince.Interval,
        tags: dict[str, str],
    ) -> tuple[int, int]:
        return start_time, end_time

    @classmethod
    async def async_collect_df(
        cls,
        start_time: int,
        end_time: int,
        interval: mince.Interval,
        tags: dict[str, str],
    ) -> pl.DataFrame:
        raise NotImplementedError()

    @classmethod
    async def async_collect_data(
        cls,
        data_dir: str,
        start_time: float,
        end_time: float,
        intervals: list[mince.Interval],
        skip_incomplete_intervals: bool,
        extra_kwargs: dict[str, typing.Any],
        verbose: int,
        dry: bool,
    ) -> dict[str, pl.DataFrame]:
        return await mince.ops.async_collect_data_piecewise(
            data_dir=data_dir,
            start_time=start_time,
            end_time=end_time,
            intervals=intervals,
            skip_incomplete_intervals=skip_incomplete_intervals,
            chunk_size=extra_kwargs['chunk_size'],
            skip_existing_files=extra_kwargs['skip_existing_files'],
            max_concurrent_queries=extra_kwargs['max_concurrent_queries'],
            async_collect_df=cls.async_collect_df,
            get_chunk_time_range=cls.get_chunk_time_range,
            path_template=cls.path_template,
            tags={
                tag_name: extra_kwargs[tag_name] for tag_name in cls.tag_names
            },
            verbose=verbose,
            dry=dry,
        )
