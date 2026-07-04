"""The sample Polars dataframes now live in itables_core.sample_polars_dfs"""

import sys

import itables_core.sample_polars_dfs as _sample_polars_dfs

sys.modules[__name__] = _sample_polars_dfs
