"""The sample dataframes now live in itables_core.sample_dfs"""

import sys

import itables_core.sample_dfs as _sample_dfs

sys.modules[__name__] = _sample_dfs
