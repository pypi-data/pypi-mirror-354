"""mince is a toolkit for slicing up data into bite-sized dashboards"""

__version__ = '0.2.4'

import typing

from .dashboards import Dashboard
from .ops import async_collect_dashboard_data, run_dashboard
from .ops.collection.collection_piecewise import PiecewiseCollector

if typing.TYPE_CHECKING:
    from .types import *
