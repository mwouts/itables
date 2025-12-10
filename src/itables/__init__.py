from itables import config, downsample, options, sample_dfs

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
    from itables import sample_pandas_dfs
except ImportError:
    sample_pandas_dfs = None

try:
    from itables import sample_polars_dfs
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
