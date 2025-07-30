
# mince 🔪🧄🧅

`mince` is a toolkit for slicing up data into bite-sized dashboards

The goal of `mince` is to minimize the effort required to build and maintain dashboards

`mince` provides a single coherent interface to help with many different dashboard-related tasks:
- ETL: data exploration, design of queries, execution of queries, persistent data storage
- UI: data visualization, custom interactive buttons
- hosting: building images, deploying images, network configuration
- live updates: collecting, storing, and serving data diffs efficiently

#### Table Of Contents
1. [Getting started](#getting-started)
2. [Data Collection](#data-collection)
3. [UI Specification](#ui-specification)
4. [Command Line Interface](#command-line-interface)


## Getting started

#### 1. Installation

```console
pip install mince
```

#### 2. Define a new `Dashboard` class

Every `mince` dashboard needs 1) a data collector function and 2) a specification for how to display data

```python
from mince import Dashboard, CollectKwargs, UiSpec
import polars as pl


class SomeNewDash(Dashboard):
    @classmethod
    async def async_collect_data(cls, **kwargs: Unpack[CollectKwargs]) -> dict[str, pl.DataFrame]:
        ...

    @classmethod
    def load_spec(cls) -> UiSpec:
        ...
```

#### 3. (optional) Register dashboard

Adding a dashboard to the local registry makes it possible to refer to dashboards by name instead of by class

python:
```python
mince.register(SomeNewDash)
```

cli:
```console
mince register some_module_name.SomeNewDash
````


#### 4. Collect dashboard data

The collector function should return a dict of polars dataframes, which `mince` will then store in its data directory.

python:
```python
await mince.async_collect_dashboard_data(SomeNewDash)
# or, if registered: mince.async_collect_dashboard_data('some_new_dash')
```

cli:
```console
mince collect some_new_dash
```

#### 5. Run dashboard

Running the dashboard loads the most recently collected data and serves a UI on a local port (such as http://localhost:8052)

python:
```python
mince.run_dashboard(SomeNewDash)
# or, if registered: mince.run_dashboard('some_new_dash')
```

cli:
```console
mince run some_new_dash
```

### Environment

- `MINCE_ROOT` root directory where mince stores collected data, default `~/data/mince`
- `MINCE_REGISTRY` path to mince registry, default `MINCE_ROOT/mince_registry.json`

## Data Collection

[WIP]

### Data storage

Design goals
- use same path structure for local filesystem vs web urls
- allow atomic updates for groups of files

## UI Specification

[WIP]

## Command Line Interface

The `mince` cli aims to automate as many of these tasks as possible

- run dashboard
    `mince run ... --pdb`
- run dashboard with interactive debugger
    `mince run ... --pdb`
- list info about all running dashboards
    - `mince ls`
- disk caching of loaded datasets for quick dashboard restarts
- standardized hooks for data collection
    `mince collect <DASHBOARD>`
- cli generator to create a management cli for each dashboard
    `<DASHBOARD> <SUBCOMMAND> ...`
- easily load a dashboard's data into an interactive python session
    `mince data <DASHBOARD> -i`

### Custom CLI's
- bypasses the registry
- takes config settings using arguments
- is meant to be intended within each dashboard package
