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
#     display_name: python3
#     language: python
#     name: python3
# ---

# %% tags=["remove-cell"]
# pyright: reportUnusedExpression=false

# %% [markdown]
# # Markdown preview - Pandas dataframes
#
# `itables.to_markdown_table()` returns the Markdown table that `itables.show()`
# prints when it can't display an interactive table at all - see
# [Markdown preview](markdown_preview.md) for why, and when, this is
# shown. This page shows it for each of our test Pandas dataframes; see
# [Pandas dataframes](../pandas_dataframes.md) for the same dataframes rendered
# as interactive tables.

# %%
import itables

dict_of_test_dfs = itables.sample_pandas_dfs.get_dict_of_test_dfs()

# %% [markdown]
# ## empty

# %%
print(itables.to_markdown_table(dict_of_test_dfs["empty"]))

# %% [markdown]
# ## No rows

# %%
print(itables.to_markdown_table(dict_of_test_dfs["no_rows"]))

# %% [markdown]
# ## No columns

# %%
print(itables.to_markdown_table(dict_of_test_dfs["no_columns"]))

# %% [markdown]
# ## No rows one column

# %%
print(itables.to_markdown_table(dict_of_test_dfs["no_rows_one_column"]))

# %% [markdown]
# ## No columns one row

# %%
print(itables.to_markdown_table(dict_of_test_dfs["no_columns_one_row"]))

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
# ## ordered_categories_in_multiindex

# %%
print(itables.to_markdown_table(dict_of_test_dfs["ordered_categories_in_multiindex"]))

# %% [markdown]
# ## object

# %%
print(itables.to_markdown_table(dict_of_test_dfs["object"]))

# %% [markdown]
# ## multiindex

# %%
print(itables.to_markdown_table(dict_of_test_dfs["multiindex"]))

# %% [markdown]
# ## countries

# %%
print(itables.to_markdown_table(dict_of_test_dfs["countries"]))

# %% [markdown]
# ## capital

# %%
print(itables.to_markdown_table(dict_of_test_dfs["capital"]))

# %% [markdown]
# ## complex_index

# %%
print(itables.to_markdown_table(dict_of_test_dfs["complex_index"]))

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
# ## sorted_index

# %%
print(itables.to_markdown_table(dict_of_test_dfs["sorted_index"]))

# %% [markdown]
# ## reverse_sorted_index

# %%
print(itables.to_markdown_table(dict_of_test_dfs["reverse_sorted_index"]))

# %% [markdown]
# ## sorted_multiindex

# %%
print(itables.to_markdown_table(dict_of_test_dfs["sorted_multiindex"]))

# %% [markdown]
# ## unsorted_index

# %%
print(itables.to_markdown_table(dict_of_test_dfs["unsorted_index"]))

# %% [markdown]
# ## duplicated_columns

# %%
print(itables.to_markdown_table(dict_of_test_dfs["duplicated_columns"]))

# %% [markdown]
# ## named_column_index

# %%
print(itables.to_markdown_table(dict_of_test_dfs["named_column_index"]))

# %% [markdown]
# ## big_integers

# %%
print(itables.to_markdown_table(dict_of_test_dfs["big_integers"]))
