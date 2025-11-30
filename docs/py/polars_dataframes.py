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
# # Polars dataframes
#
# In this notebook we make sure that our test [Polars](https://www.pola.rs/)
# dataframes are displayed nicely with the default `itables` settings.

# %%
import itables

dict_of_test_dfs = itables.sample_dfs.get_dict_of_polars_test_dfs()
itables.init_notebook_mode()

# %% [markdown]
# ## empty

# %%
itables.show(dict_of_test_dfs["empty"])

# %% [markdown]
# ## No rows

# %%
itables.show(dict_of_test_dfs["no_rows"])

# %% [markdown]
# ## No rows one column

# %%
itables.show(dict_of_test_dfs["no_rows_one_column"])

# %% [markdown]
# ## No columns

# %%
itables.show(dict_of_test_dfs["no_columns"])

# %% [markdown]
# ## No columns one row

# %%
itables.show(dict_of_test_dfs["no_columns_one_row"])

# %% [markdown]
# ## bool

# %%
itables.show(dict_of_test_dfs["bool"])

# %% [markdown]
# ## Nullable boolean

# %%
itables.show(dict_of_test_dfs["nullable_boolean"])

# %% [markdown]
# ## int

# %%
itables.show(dict_of_test_dfs["int"])

# %% [markdown]
# ## Nullable integer

# %%
itables.show(dict_of_test_dfs["nullable_int"])

# %% [markdown]
# ## float

# %%
itables.show(dict_of_test_dfs["float"])

# %% [markdown]
# ## str

# %%
itables.show(dict_of_test_dfs["str"])

# %% [markdown]
# ## time

# %%
itables.show(dict_of_test_dfs["time"])

# %% [markdown]
# ## ordered_categories

# %%
itables.show(dict_of_test_dfs["ordered_categories"])

# %% [markdown]
# ## countries

# %% tags=["full-width"]
itables.show(dict_of_test_dfs["countries"])

# %% [markdown]
# ## capital

# %%
itables.show(dict_of_test_dfs["capital"])

# %% [markdown]
# ## int_float_str

# %%
itables.show(dict_of_test_dfs["int_float_str"])

# %% [markdown]
# ## wide

# %% tags=["full-width"]
itables.show(dict_of_test_dfs["wide"], maxBytes=100000, maxColumns=100)

# %% [markdown]
# ## long_column_names

# %% tags=["full-width"]
itables.show(dict_of_test_dfs["long_column_names"])

# %% [markdown]
# ## named_column_index

# %%
itables.show(dict_of_test_dfs["named_column_index"])

# %% [markdown]
# ## big_integers

# %%
itables.show(dict_of_test_dfs["big_integers"])
