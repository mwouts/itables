# ---
# jupyter:
#   jupytext:
#     default_lexer: ipython3
#     formats: docs///md:myst,docs/py///py:percent
#     notebook_metadata_filter: -jupytext.text_representation.jupytext_version
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#   kernelspec:
#     display_name: itables
#     language: python
#     name: itables
# ---

# %% [markdown]
# # Column Filters
#
# ```{tip}
# Since v2.5.0, ITables include the [ColumnControl](column_control.md) extension, which provide the same functionality as the column filters,
# and much more!
# ```
#
# Use `column_filters = "header"` or `"footer"` if you wish to display individual column filters
# (remove the global search box with a [`layout`](layout) modifier if desired).

# %%
import pandas as pd

import itables

itables.init_notebook_mode()

alpha_numeric_df = pd.DataFrame(
    [["one", 1.5], ["two", 2.3]], columns=["string", "numeric"]
)

itables.show(alpha_numeric_df, column_filters="header", layout={"topEnd": None})

# %% [markdown]
# As always you can set activate column filters by default with e.g.

# %%
itables.options.column_filters = "footer"

# %% [markdown]
# Column filters also work on dataframes with multiindex columns:

# %%
itables.sample_dfs.get_dict_of_test_dfs()["multiindex"]

# %% tags=["remove-cell"]
# Revert back to the default to avoid interactions with the tests
itables.options.column_filters = False
