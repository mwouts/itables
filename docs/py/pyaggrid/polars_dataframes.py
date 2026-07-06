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
# dataframes are displayed nicely with the default `pyaggrid` settings.
#
# import itables_core.sample_polars_dfs

# %%
import polars as pl  # noqa: F401
import pyaggrid

dict_of_test_dfs = itables_core.sample_polars_dfs.get_dict_of_test_dfs()

# %% [markdown]
# ## empty

# %%
pyaggrid.show(dict_of_test_dfs["empty"])

# %% [markdown]
# ## No rows

# %%
pyaggrid.show(dict_of_test_dfs["no_rows"])

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
    pl.DataFrame(
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
# ## ordered_categories

# %%
pyaggrid.show(dict_of_test_dfs["ordered_categories"])

# %% [markdown]
# ## countries

# %% tags=["full-width"]
pyaggrid.show(dict_of_test_dfs["countries"])

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
# ## big_integers

# %%
pyaggrid.show(dict_of_test_dfs["big_integers"])
