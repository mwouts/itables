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

# %% tags=["remove-cell"]
# pyright: reportUnusedExpression=false

# %% [markdown]
# # Markdown preview - Polars dataframes
#
# `itables.to_markdown_table()` returns the Markdown table that `itables.show()`
# prints when it can't display an interactive table at all - see
# [Markdown preview](markdown_preview.md) for why, and when, this is
# shown. This page shows it for each of our test [Polars](https://www.pola.rs/)
# dataframes; see [Polars dataframes](../polars_dataframes.md) for the same
# dataframes rendered as interactive tables.

# %%
import itables

dict_of_test_dfs = itables.sample_polars_dfs.get_dict_of_test_dfs()

# %% [markdown]
# ## empty

# %%
print(itables.to_markdown_table(dict_of_test_dfs["empty"]))

# %% [markdown]
# ## No rows

# %%
print(itables.to_markdown_table(dict_of_test_dfs["no_rows"]))

# %% [markdown]
# ## bool

# %%
print(itables.to_markdown_table(dict_of_test_dfs["bool"]))

# %% [markdown]
# ## Nullable boolean

# %%
print(itables.to_markdown_table(dict_of_test_dfs["nullable_boolean"]))

# %% [markdown]
# ## int

# %%
print(itables.to_markdown_table(dict_of_test_dfs["int"]))

# %% [markdown]
# ## Nullable integer

# %%
print(itables.to_markdown_table(dict_of_test_dfs["nullable_int"]))

# %% [markdown]
# ## float

# %%
print(itables.to_markdown_table(dict_of_test_dfs["float"]))

# %% [markdown]
# ## float_types

# %%
print(itables.to_markdown_table(dict_of_test_dfs["float_types"]))

# %% [markdown]
# ## str

# %%
print(itables.to_markdown_table(dict_of_test_dfs["str"]))

# %% [markdown]
# ## time

# %%
print(itables.to_markdown_table(dict_of_test_dfs["time"]))

# %% [markdown]
# ## date_range

# %%
print(itables.to_markdown_table(dict_of_test_dfs["date_range"]))

# %% [markdown]
# ## ordered_categories

# %%
print(itables.to_markdown_table(dict_of_test_dfs["ordered_categories"]))

# %% [markdown]
# ## object

# %%
print(itables.to_markdown_table(dict_of_test_dfs["object"]))

# %% [markdown]
# ## countries

# %%
print(itables.to_markdown_table(dict_of_test_dfs["countries"]))

# %% [markdown]
# ## int_float_str

# %%
print(itables.to_markdown_table(dict_of_test_dfs["int_float_str"]))

# %% [markdown]
# ## wide

# %%
print(itables.to_markdown_table(dict_of_test_dfs["wide"]))

# %% [markdown]
# ## long_column_names

# %%
print(itables.to_markdown_table(dict_of_test_dfs["long_column_names"]))

# %% [markdown]
# ## big_integers

# %%
print(itables.to_markdown_table(dict_of_test_dfs["big_integers"]))
