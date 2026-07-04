"""The sample Pandas dataframes now live in itables_core.sample_pandas_dfs"""

import sys

import itables_core.sample_pandas_dfs as _sample_pandas_dfs

sys.modules[__name__] = _sample_pandas_dfs
