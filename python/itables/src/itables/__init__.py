"""itables: the backward-compatible interface to pydatatables

The itables package was split into pydatatables (the DataTables renderer),
pyaggrid (the AG Grid renderer) and itables_core (the shared core functions).

This package lets you keep using the historical itables API:
the functions and classes below are re-exported from pydatatables
under their original names.
"""

from pydatatables import config, downsample, options, sample_dfs

from .javascript import init_notebook_mode, show, to_html_datatable
from .typing import (
    DataFrameOrSeries,
    DTForITablesOptions,
    ITableOptions,
    JavascriptCode,
    JavascriptFunction,
)
from .version import __version__

try:
    from pydatatables import sample_pandas_dfs
except ImportError:
    sample_pandas_dfs = None

try:
    from pydatatables import sample_polars_dfs
except ImportError:
    sample_polars_dfs = None

__all__ = [
    "__version__",
    "to_html_datatable",
    "show",
    "init_notebook_mode",
    "JavascriptCode",
    "JavascriptFunction",
    "DataFrameOrSeries",
    "ITableOptions",
    "DTForITablesOptions",
    "config",
    "options",
    "downsample",
    "sample_dfs",
    "sample_pandas_dfs",
    "sample_polars_dfs",
]
