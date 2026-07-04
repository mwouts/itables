"""itables_core: the functions shared by the ITables packages (pydatatables, pyaggrid)

This package provides the dataframe-related logic that is common to the
DataTables and AG Grid renderers: downsampling, row formatting/serialization,
dataframe typing helpers and the sample dataframes.
"""

from itables_core import downsample, formatting, frames, sample_dfs, typing, utils

from .downsample import downsample as downsample_df
from .formatting import datatables_rows, escape_html_chars
from .frames import evaluate_show_index, safe_reset_index
from .typing import (
    DataFrameOrSeries,
    JavascriptCode,
    JavascriptFunction,
)
from .version import __version__

try:
    from itables_core import sample_pandas_dfs
except ImportError:
    sample_pandas_dfs = None

try:
    from itables_core import sample_polars_dfs
except ImportError:
    sample_polars_dfs = None

__all__ = [
    "__version__",
    "DataFrameOrSeries",
    "JavascriptCode",
    "JavascriptFunction",
    "datatables_rows",
    "downsample",
    "downsample_df",
    "escape_html_chars",
    "evaluate_show_index",
    "formatting",
    "frames",
    "safe_reset_index",
    "sample_dfs",
    "sample_pandas_dfs",
    "sample_polars_dfs",
    "typing",
    "utils",
]
