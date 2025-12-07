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
# ruff: noqa: E402
# pyright: reportUnusedExpression=false

# %% [markdown]
# # Widget
#
# The `ITable` widget depends on [AnyWidget](https://anywidget.dev) -
# a great widget development framework! You can install it with
# ```bash
# pip install itables[widget]
# ```
#
# The `ITable` class accepts the same [options](../options/options.md) as the `show` method, but
# the `df` argument is optional.

# %%
from itables.sample_pandas_dfs import get_dict_of_test_dfs
from itables.widget import ITable

df = get_dict_of_test_dfs()["int_float_str"]

table = ITable(df, selected_rows=[0, 2, 5], select=True)
table

# %% [markdown]
# ```{tip}
# The table shown above does not reflect the initial row selection.
# This is because the `ITable` widget was updated with
# more row selection commands, see below.
# ```
#
# ## The `selected_rows` traits
#
# The `selected_rows` attribute of the `ITable` object provides a view on the
# rows that have been selected in the table (remember to pass [`select=True`](../options/select.md) to activate the row selection). You can use it to either retrieve
# or change the current row selection:

# %%
table.selected_rows

# %%
table.selected_rows = [3, 4]

# %% [markdown]
# ## The `df` property
#
# Use it to retrieve the table data:

# %%
table.df.iloc[table.selected_rows]

# %% [markdown]
# or to update it

# %%
table.df = df.head(6)

# %% [markdown]
# ```{tip}
# `ITable` raises an `IndexError` if the `selected_rows` are not consistent with the data. If you need to update both simultaneously, use `table.update(df, selected_rows=...)`, see below.
# ```
#
# ## The `caption`, `style` and `classes` traits
#
# You can update these traits from Python, e.g.

# %%
table.caption = "numbers and strings"

# %% [markdown]
# ## The `update` method
#
# Last but not least, you can update the `ITable` arguments simultaneously using the `update` method:

# %%
table.update(df.head(20), selected_rows=[7, 8])

# %% [markdown]
# ## Using HTML
#
# An alternative to the widget, if you only want to _display_ the table, is the `show` function. Below is an example in which we use `show` to display a different table depending on the value of a drop-down component:
#
# ```python
# import ipywidgets as widgets
# from itables import show
# from itables.sample_dfs import get_dict_of_test_dfs
#
# def use_show_in_interactive_output(table_name: str):
#     show(
#         sample_dfs[table_name],
#         caption=table_name,
#     )
#
# sample_dfs = get_dict_of_test_dfs()
# table_selector = widgets.Dropdown(options=sample_dfs.keys(), value="int_float_str")
#
# out = widgets.interactive_output(
#     use_show_in_interactive_output, {"table_name": table_selector}
# )
#
# widgets.VBox([table_selector, out])
# ```
