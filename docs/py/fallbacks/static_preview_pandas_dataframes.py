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
# pyright: reportUnknownVariableType=false

# %% [markdown]
# # Static preview - Pandas dataframes
#
# `itables.to_html_static_preview()` returns the plain HTML table that
# `to_html_datatable()` shows by default, ahead of the interactive table -
# see [Static preview](static_preview.md) for why, and when, this is shown
# instead. This page shows it for each of our test
# Pandas dataframes; see [Pandas dataframes](../pandas_dataframes.md) for the
# same dataframes rendered as interactive tables.

# %%
from IPython.display import HTML, display

import itables

dict_of_test_dfs = itables.sample_pandas_dfs.get_dict_of_test_dfs()

# %% [markdown]
# ## empty

# %%
display(HTML(itables.to_html_static_preview(dict_of_test_dfs["empty"])))

# %% [markdown]
# ## No rows

# %%
display(HTML(itables.to_html_static_preview(dict_of_test_dfs["no_rows"])))

# %% [markdown]
# ## No columns

# %%
display(HTML(itables.to_html_static_preview(dict_of_test_dfs["no_columns"])))

# %% [markdown]
# ## No rows one column

# %%
display(HTML(itables.to_html_static_preview(dict_of_test_dfs["no_rows_one_column"])))

# %% [markdown]
# ## No columns one row

# %%
display(HTML(itables.to_html_static_preview(dict_of_test_dfs["no_columns_one_row"])))

# %% [markdown]
# ## bool

# %%
display(HTML(itables.to_html_static_preview(dict_of_test_dfs["bool"])))

# %% [markdown]
# ## Nullable boolean

# %%
display(HTML(itables.to_html_static_preview(dict_of_test_dfs["nullable_boolean"])))

# %% [markdown]
# ## int

# %%
display(HTML(itables.to_html_static_preview(dict_of_test_dfs["int"])))

# %% [markdown]
# ## Nullable integer

# %%
display(HTML(itables.to_html_static_preview(dict_of_test_dfs["nullable_int"])))

# %% [markdown]
# ## float

# %%
display(HTML(itables.to_html_static_preview(dict_of_test_dfs["float"])))

# %% [markdown]
# ## float_types

# %%
display(HTML(itables.to_html_static_preview(dict_of_test_dfs["float_types"])))

# %% [markdown]
# ## str

# %%
display(HTML(itables.to_html_static_preview(dict_of_test_dfs["str"])))

# %% [markdown]
# ## time

# %%
display(HTML(itables.to_html_static_preview(dict_of_test_dfs["time"])))

# %% [markdown]
# ## date_range

# %%
display(HTML(itables.to_html_static_preview(dict_of_test_dfs["date_range"])))

# %% [markdown]
# ## ordered_categories

# %%
display(HTML(itables.to_html_static_preview(dict_of_test_dfs["ordered_categories"])))

# %% [markdown]
# ## ordered_categories_in_multiindex

# %%
display(
    HTML(
        itables.to_html_static_preview(
            dict_of_test_dfs["ordered_categories_in_multiindex"]
        )
    )
)

# %% [markdown]
# ## object

# %%
display(HTML(itables.to_html_static_preview(dict_of_test_dfs["object"])))

# %% [markdown]
# ## multiindex

# %%
display(HTML(itables.to_html_static_preview(dict_of_test_dfs["multiindex"])))

# %% [markdown]
# ## countries

# %% tags=["full-width"]
display(HTML(itables.to_html_static_preview(dict_of_test_dfs["countries"])))

# %% [markdown]
# ## capital

# %%
display(HTML(itables.to_html_static_preview(dict_of_test_dfs["capital"])))

# %% [markdown]
# ## complex_index

# %% tags=["full-width"]
display(HTML(itables.to_html_static_preview(dict_of_test_dfs["complex_index"])))

# %% [markdown]
# ## int_float_str

# %%
display(HTML(itables.to_html_static_preview(dict_of_test_dfs["int_float_str"])))

# %% [markdown]
# ## wide

# %% tags=["full-width"]
display(HTML(itables.to_html_static_preview(dict_of_test_dfs["wide"])))

# %% [markdown]
# ## long_column_names

# %% tags=["full-width"]
display(HTML(itables.to_html_static_preview(dict_of_test_dfs["long_column_names"])))

# %% [markdown]
# ## sorted_index

# %%
display(HTML(itables.to_html_static_preview(dict_of_test_dfs["sorted_index"])))

# %% [markdown]
# ## reverse_sorted_index

# %%
display(HTML(itables.to_html_static_preview(dict_of_test_dfs["reverse_sorted_index"])))

# %% [markdown]
# ## sorted_multiindex

# %%
display(HTML(itables.to_html_static_preview(dict_of_test_dfs["sorted_multiindex"])))

# %% [markdown]
# ## unsorted_index

# %%
display(HTML(itables.to_html_static_preview(dict_of_test_dfs["unsorted_index"])))

# %% [markdown]
# ## duplicated_columns

# %%
display(HTML(itables.to_html_static_preview(dict_of_test_dfs["duplicated_columns"])))

# %% [markdown]
# ## named_column_index

# %%
display(HTML(itables.to_html_static_preview(dict_of_test_dfs["named_column_index"])))

# %% [markdown]
# ## big_integers

# %%
display(HTML(itables.to_html_static_preview(dict_of_test_dfs["big_integers"])))
