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
# # Pandas dataframes
#
# In this notebook we make sure that our test dataframes are displayed nicely with the default `pyaggrid` settings.
#
# import itables_core.sample_pandas_dfs

# %%
import pandas as pd  # noqa: F401
import pyaggrid

dict_of_test_dfs = itables_core.sample_pandas_dfs.get_dict_of_test_dfs()

# %% [markdown]
# ## empty

# %%
pyaggrid.show(dict_of_test_dfs["empty"])

# %% [markdown]
# ## No rows

# %%
pyaggrid.show(dict_of_test_dfs["no_rows"])

# %% [markdown]
# ## No rows one column

# %%
pyaggrid.show(dict_of_test_dfs["no_rows_one_column"])

# %% [markdown]
# ## No columns

# %%
pyaggrid.show(dict_of_test_dfs["no_columns"])

# %% [markdown]
# ## No columns one row

# %%
pyaggrid.show(dict_of_test_dfs["no_columns_one_row"])

# %% [markdown]
# ## bool

# %%
pyaggrid.show(dict_of_test_dfs["bool"])

# %% [markdown]
# ## Nullable boolean

# %%
pyaggrid.show(dict_of_test_dfs["nullable_boolean"])

# %% [markdown]
# ## int

# %%
pyaggrid.show(dict_of_test_dfs["int"])

# %% [markdown]
# ## Nullable integer

# %%
pyaggrid.show(dict_of_test_dfs["nullable_int"])

# %% [markdown]
# ## float

# %%
pyaggrid.show(dict_of_test_dfs["float"])

# %% [markdown]
# ## float_types

# %%
pyaggrid.show(dict_of_test_dfs["float_types"])

# %% [markdown]
# ## Ordered floats

# %%
pyaggrid.show(
    pd.DataFrame(
        {"float": [float("nan"), float("inf")] + [float(x) for x in range(18)]}
    ),
    order=[[0, "asc"]],
)

# %% [markdown]
# ## str

# %%
pyaggrid.show(dict_of_test_dfs["str"])

# %% [markdown]
# ## time

# %%
pyaggrid.show(dict_of_test_dfs["time"])

# %% [markdown]
# ## object

# %%
pyaggrid.show(dict_of_test_dfs["object"])

# %% [markdown]
# ## ordered_categories

# %%
pyaggrid.show(dict_of_test_dfs["ordered_categories"])

# %% [markdown]
# ## ordered_categories_in_multiindex

# %%
pyaggrid.show(dict_of_test_dfs["ordered_categories_in_multiindex"])

# %% [markdown]
# ## multiindex

# %%
pyaggrid.show(dict_of_test_dfs["multiindex"])

# %% [markdown]
# ## countries

# %% tags=["full-width"]
pyaggrid.show(dict_of_test_dfs["countries"])

# %% [markdown]
# ## capital

# %%
pyaggrid.show(dict_of_test_dfs["capital"])

# %% [markdown]
# ## complex_index

# %% tags=["full-width"]
pyaggrid.show(dict_of_test_dfs["complex_index"])

# %% [markdown]
# ## int_float_str

# %%
pyaggrid.show(dict_of_test_dfs["int_float_str"])

# %% [markdown]
# ## wide

# %% tags=["full-width"]
pyaggrid.show(dict_of_test_dfs["wide"], maxBytes=100000, maxColumns=100)

# %% [markdown]
# ## long_column_names

# %% tags=["full-width"]
pyaggrid.show(dict_of_test_dfs["long_column_names"])

# %% [markdown]
# ## duplicated_columns

# %%
pyaggrid.show(dict_of_test_dfs["duplicated_columns"])

# %% [markdown]
# ## named_column_index

# %%
pyaggrid.show(dict_of_test_dfs["named_column_index"])

# %% [markdown]
# ## big_integers

# %%
pyaggrid.show(dict_of_test_dfs["big_integers"])
