from __future__ import annotations

from typing import Mapping, Sequence, TYPE_CHECKING

import mince.schemas
from . import spec_create

if TYPE_CHECKING:
    import polars as pl
    from mince import types


def create_default_ui_spec(
    *,
    name: str,
    title: str | None = None,
    description: str | None = None,
    favicon_emoji: str | None = None,
    version: str,
    df: pl.DataFrame | None = None,
    metrics: dict[str, types.MetricSpec],
    default_inputs: dict[str, mince.StateDatum | None],
    metric_aliases: dict[str, types.StateDatum],
    submetrics: Mapping[str, Sequence[str]],
    grouping_aliases: dict[str, str],
    colors: dict[str, str],
    add_shortcuts: dict[str, types.ShortcutSpec] | None = None,
    schema: types.DataSchemaPartial | None = None,
    title_prefix: str | None = None,
    title_infix: str | None = None,
    title_postfix: str | None = None,
) -> types.UiSpec:
    inputs, metric_selectors = _get_default_inputs(
        metric_aliases=metric_aliases,
        metrics=metrics,
        grouping_aliases=grouping_aliases,
        submetrics=submetrics,
        default_inputs=default_inputs,
    )

    if metric_aliases is not None:
        inputs['metric']['aliases'] = metric_aliases
        inputs['submetric']['aliases'] = metric_aliases

    shortcuts = _get_default_shortcuts()
    if add_shortcuts is not None:
        shortcuts.update(add_shortcuts)

    if schema is None:
        schema = {'columns': mince.schemas.get_default_columns()}  # type: ignore
    schema_whole = mince.schemas.partial_schema_to_whole(schema)

    return spec_create.create_ui_spec(
        name=name,
        title=title,
        description=description,
        favicon_emoji=favicon_emoji,
        version=version,
        groupings=list(grouping_aliases.values()),
        invalid_states=_get_default_invalid_states(
            metrics=metrics,
            metric_selectors=metric_selectors,
        ),
        inputs=inputs,
        metrics=metrics,
        submetrics=submetrics,
        shortcuts=shortcuts,
        colors=colors,
        schema=schema_whole,
        title_prefix=title_prefix,
        title_infix=title_infix,
        title_postfix=title_postfix,
    )


def _get_default_invalid_states(
    metrics: dict[str, types.MetricSpec],
    metric_selectors: dict[str, dict[str, types.StateDatum]],
) -> list[dict[str, types.StateDatum]]:
    combos: list[dict[str, types.StateDatum]] = []

    line_only_values: list[dict[str, types.StateDatum]] = [
        {'yscale': 'log'},
        {'xalign': 'age'},
        {'ynormalize': 'relative'},
        {'total': 'total'},
    ]
    for value in line_only_values:
        for format in ['line %', 'area', 'area %', 'tree']:
            bad = value.copy()
            bad['format'] = format
            combos.append(bad)

    # only use total when metric type == 'sum'
    for metric, metric_spec in metrics.items():
        if metric_spec['type'] != 'sum':
            combo = dict(metric_selectors[metric], total='total')
            combos.append(combo)

    combos.extend(
        [
            {'time_window': '7d', 'sample_interval': 'monthly'},
            {'time_window': '7d', 'sample_interval': 'weekly'},
            {'time_window': '30d', 'sample_interval': 'monthly'},
        ]
    )

    combos.extend(
        [
            {'xalign': 'age', 'ynormalize': 'relative'},
            {'xalign': 'age', 'total': 'total'},
        ]
    )

    return combos


def _get_default_shortcuts() -> dict[str, types.ShortcutSpec]:
    return {
        '[': {'action': 'cycle_previous', 'field': 'metric'},
        ']': {'action': 'cycle_next', 'field': 'metric'},
        '{': {'action': 'cycle_previous', 'field': 'submetric'},
        '}': {'action': 'cycle_next', 'field': 'submetric'},
        'L': {'action': 'select', 'field': 'format', 'value': 'line'},
        'P': {'action': 'select', 'field': 'format', 'value': 'line %'},
        'A': {'action': 'select', 'field': 'format', 'value': 'area'},
        'p': {'action': 'select', 'field': 'format', 'value': 'area %'},
        'T': {'action': 'select', 'field': 'format', 'value': 'tree'},
        'w': {'action': 'select', 'field': 'time_window', 'value': '7d'},
        'm': {'action': 'select', 'field': 'time_window', 'value': '30d'},
        'y': {'action': 'select', 'field': 'time_window', 'value': '365d'},
        'a': {'action': 'select', 'field': 'time_window', 'value': 'all'},
        'D': {'action': 'select', 'field': 'sample_interval', 'value': 'daily'},
        'W': {
            'action': 'select',
            'field': 'sample_interval',
            'value': 'weekly',
        },
        'M': {
            'action': 'select',
            'field': 'sample_interval',
            'value': 'monthly',
        },
        'l': {
            'action': 'cycle_next',
            'field': 'yscale',
            'help': 'toggle log yaxis',
        },
        'r': {
            'action': 'cycle_next',
            'field': 'ynormalize',
            'help': 'toggle relative yxaxis',
        },
        'x': {
            'action': 'cycle_next',
            'field': 'xalign',
            'help': 'toggle age xaxis',
        },
        'ArrowLeft': {
            'action': 'decrement',
            'field': 'now',
            'value': 'large',
            'help': 'move backward in time',
        },
        'ArrowRight': {
            'action': 'increment',
            'field': 'now',
            'value': 'large',
            'help': 'move forward in time',
        },
        'H': {
            'action': 'toggle_ui',
            'field': 'radio_group_visibility',
            'help': 'toggle button visibility',
        },
        '?': {
            'action': 'toggle_ui',
            'field': 'help_open',
            'help': 'toggle help',
        },
        'h': {
            'action': 'toggle_ui',
            'field': 'help_open',
            'help': 'toggle help',
        },
    }


def _get_default_inputs(
    *,
    metric_aliases: dict[str, types.StateDatum],
    metrics: dict[str, types.MetricSpec],
    grouping_aliases: dict[str, str],
    default_inputs: dict[str, mince.StateDatum | None],
    submetrics: Mapping[str, Sequence[str]],
) -> tuple[dict[str, types.InputSpec], dict[str, dict[str, types.StateDatum]]]:
    default_metric = default_inputs['metric']
    if default_metric is None:
        default_metric = list(metrics.keys())[0]
    if not isinstance(default_metric, str):
        raise Exception('could not determine default metric')

    # default time window
    raw_default_time_window = default_inputs.get('time_window')
    if raw_default_time_window is None:
        default_time_window = 'all'
    elif isinstance(raw_default_time_window, str):
        default_time_window = raw_default_time_window
    else:
        raise Exception('invalid type for default_time_window')

    # default format
    raw_default_format = default_inputs.get('format')
    if raw_default_format is None:
        default_format = 'line'
    elif isinstance(raw_default_format, str):
        default_format = raw_default_format
    else:
        raise Exception('invalid type for default_format')

    # yscale
    raw_default_yscale = default_inputs.get('yscale')
    if raw_default_yscale is None:
        default_yscale = 'linear'
    elif isinstance(raw_default_yscale, str):
        default_yscale = raw_default_yscale
    else:
        raise Exception('invalid type for default_yscale')

    # ynormalize
    raw_default_ynormalize = default_inputs.get('ynormalize')
    if raw_default_ynormalize is None:
        default_ynormalize = 'absolute'
    elif isinstance(raw_default_ynormalize, str):
        default_ynormalize = raw_default_ynormalize
    else:
        raise Exception('invalid type for default_ynormalize')

    # xalign
    raw_default_xalign = default_inputs.get('xalign')
    if raw_default_xalign is None:
        default_xalign = 'time'
    elif isinstance(raw_default_xalign, str):
        default_xalign = raw_default_xalign
    else:
        raise Exception('invalid type for default_xalign')

    # cumulative
    raw_default_cumulative = default_inputs.get('cumulative')
    if raw_default_cumulative is None:
        default_cumulative = 'non-cumulative'
    elif isinstance(raw_default_cumulative, str):
        default_cumulative = raw_default_cumulative
    else:
        raise Exception('invalid type for default_cumulative')

    # total
    raw_default_total = default_inputs.get('cumulative')
    if raw_default_total is None:
        default_total = 'no total'
    elif isinstance(raw_default_total, str):
        default_total = raw_default_total
    else:
        raise Exception('invalid type for default_total')

    # hover
    raw_default_hover = default_inputs.get('cumulative')
    if raw_default_hover is None:
        default_hover = 'hover'
    elif isinstance(raw_default_hover, str):
        default_hover = raw_default_hover
    else:
        raise Exception('invalid type for default_hover')

    # default sample interval
    raw_default_sample_interval = default_inputs.get('sample_interval')
    if raw_default_sample_interval is None:
        default_sample_interval = 'weekly'
    elif isinstance(raw_default_sample_interval, str):
        default_sample_interval = raw_default_sample_interval
    else:
        raise Exception('invalid type for default_sample_interval')

    # metric options
    reverse_metric_aliases = {v: k for k, v in metric_aliases.items()}
    metric_options = []
    metric_selectors: dict[str, dict[str, types.StateDatum]] = {}
    for metric in metrics.keys():
        for submetric_category in submetrics.keys():
            if metric in submetrics[submetric_category]:
                metric_selectors[metric] = {
                    'metric': submetric_category,
                    'submetric': reverse_metric_aliases.get(metric, metric),
                }
                if submetric_category not in metric_options:
                    metric_options.append(submetric_category)
                break
        else:
            metric_selectors[metric] = {
                'metric': reverse_metric_aliases.get(metric, metric)
            }
            metric_options.append(reverse_metric_aliases.get(metric, metric))

    # get metric defaults
    for submetric_category in submetrics.keys():
        if default_metric in submetrics[submetric_category]:
            aliased_default_metric = submetric_category
            aliased_submetric_options = [
                reverse_metric_aliases.get(metric, metric)
                for metric in submetrics[submetric_category]
            ]
            aliased_default_submetric = reverse_metric_aliases.get(
                default_metric, default_metric
            )
            break
    else:
        aliased_default_metric = reverse_metric_aliases.get(
            default_metric, default_metric
        )
        if len(submetrics) > 0:
            aliased_submetric_options = list(next(iter(submetrics.values())))
            aliased_default_submetric = aliased_submetric_options[0]
        else:
            aliased_submetric_options = []
            aliased_default_submetric = None

    return {
        'now': {
            'type': 'date',
            'description': 'Select date',
            'default': None,
            'aliases': {},
        },
        'metric': {
            'type': 'button',
            'description': 'Select metric',
            'button_options': metric_options,
            'default': aliased_default_metric,
            'aliases': {},
        },
        'submetric': {
            'type': 'button',
            'description': 'Select submetric',
            'button_options': aliased_submetric_options,
            'default': aliased_default_submetric,
            'visibility': {
                'show_if': [
                    {'metric': metric_aliases.get(metric, metric)}
                    for metric in submetrics.keys()
                ]
            },
            'aliases': {},
        },
        'format': {
            'type': 'button',
            'description': 'Select chart type',
            'button_options': [
                'line',
                'line %',
                'area',
                'area %',
                'tree',
            ],
            'default': default_format,
            'aliases': {},
        },
        'time_window': {
            'type': 'button',
            'description': 'Select time window',
            'button_options': [
                '7d',
                '30d',
                '365d',
                'all',
            ],
            'default': default_time_window,
            'visibility': {
                'hide_if': [
                    dict(metric_selectors[metric], format='tree')
                    for metric, metric_spec in metrics.items()
                    if metric_spec['type'] not in ['sum', 'min', 'max']
                ],
            },
            'aliases': {},
        },
        'sample_interval': {
            'type': 'button',
            'description': 'Select sampling interval',
            'button_options': [
                'daily',
                'weekly',
                'monthly',
            ],
            'default': default_sample_interval,
            'visibility': {
                'hide_if': [
                    dict(metric_selectors[metric], format='tree')
                    for metric, metric_spec in metrics.items()
                    if metric_spec['type'] not in ['unique']
                ],
            },
            'aliases': {
                'daily': 'date',
                'weekly': 'week',
                'monthly': 'month',
            },
        },
        'grouping': {
            'type': 'button',
            'description': 'Select grouping',
            'button_options': list(grouping_aliases.keys()),
            'default': {v: k for k, v in grouping_aliases.items()}[
                default_inputs['grouping']  # type: ignore
            ],
            'aliases': grouping_aliases,  # type: ignore
            'visibility': {
                'hide': len(grouping_aliases) < 2,
            },
        },
        'yscale': {
            'type': 'button',
            'description': 'Select y-axis scale',
            'button_options': [
                'linear',
                'log',
            ],
            'default': default_yscale,
            'visibility': {
                'show_if': [{'format': 'line'}],
                'start_hidden': True,
            },
            'aliases': {},
        },
        'ynormalize': {
            'type': 'button',
            'description': 'Select y-axis normalization',
            'button_options': [
                'absolute',
                'relative',
            ],
            'default': default_ynormalize,
            'visibility': {
                'show_if': [{'format': 'line'}],
                'start_hidden': True,
            },
            'aliases': {},
        },
        'xalign': {
            'type': 'button',
            'description': 'Select x-axis alignment',
            'button_options': [
                'time',
                'age',
            ],
            'default': default_xalign,
            'visibility': {
                'show_if': [{'format': 'line'}],
                'start_hidden': True,
            },
            'aliases': {},
        },
        'cumulative': {
            'type': 'button',
            'description': 'Select whether plot is cumulative',
            'button_options': [
                'non-cumulative',
                'cumulative (window)',
                'cumulative (t=0)',
            ],
            'default': default_cumulative,
            'visibility': {
                'start_hidden': True,
                'show_if': [
                    dict(metric_selectors[metric], format='line')
                    for format in ['line', 'area']
                    for metric, metric_spec in metrics.items()
                    if metric_spec['type'] == 'sum'
                ],
            },
            'aliases': {},
        },
        'total': {
            'type': 'button',
            'description': 'Select whether to show total',
            'button_options': [
                'no total',
                'total',
            ],
            'default': default_total,
            'visibility': {
                'show_if': [
                    dict(metric_selectors[metric], format='line')
                    for metric, metric_spec in metrics.items()
                    if metric_spec['type'] == 'sum'
                ],
                'start_hidden': True,
            },
            'aliases': {},
        },
        'hover': {
            'type': 'button',
            'description': 'Select whether to show mouse hover data',
            'button_options': [
                'hover',
                'no hover',
            ],
            'default': default_hover,
            'visibility': {
                'show_if': [{'format': 'line'}],
                'start_hidden': True,
            },
            'aliases': {},
        },
    }, metric_selectors


def get_package_version(package: str) -> str:
    import importlib
    import os
    import subprocess

    module = importlib.import_module(package)
    try:
        git_branch_cmd = 'git rev-parse --abbrev-ref HEAD'
        git_commit_subcount_cmd = 'git describe --tags --abbrev=0'
        git_commit_count_cmd = 'git rev-list {subcount}..HEAD --count'
        git_tag_cmd = 'git describe --tags --abbrev=0'
        git_status_cmd = 'git diff --numstat'

        cwd = os.path.dirname(module.__file__)  # type: ignore

        tag = (
            subprocess.check_output(
                git_tag_cmd.split(' '), cwd=cwd, stderr=subprocess.DEVNULL
            )
            .decode('utf-8')
            .rstrip('\n')
        )
        subcount = (
            subprocess.check_output(git_commit_subcount_cmd.split(' '), cwd=cwd)
            .decode('utf-8')
            .rstrip('\n')
        )
        commit_count = (
            subprocess.check_output(
                git_commit_count_cmd.format(subcount=subcount).split(' '),
                cwd=cwd,
            )
            .decode('utf-8')
            .rstrip('\n')
        )
        branch = (
            subprocess.check_output(git_branch_cmd.split(' '), cwd=cwd)
            .decode('utf-8')
            .rstrip('\n')
        )
        status = (
            subprocess.check_output(git_status_cmd.split(' '), cwd=cwd)
            .decode('utf-8')
            .strip()
        )

        label = tag
        if commit_count != '0':
            label = tag + ':' + commit_count
        if branch != 'main':
            label = branch + ':' + label
        if len(status) > 0:
            n_adds = 0
            n_removes = 0
            for file in status.split('\n'):
                adds, removes, path = file.split('\t')
                n_adds += int(adds)
                n_removes += int(removes)
            if n_adds > 0:
                label = label + '+' + str(n_adds)
            if n_removes > 0:
                label = label + '-' + str(n_removes)

        return label

    except Exception:
        return module.__version__  # type: ignore
