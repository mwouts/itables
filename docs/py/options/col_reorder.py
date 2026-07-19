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

# %% [markdown]
# # Col Reorder
#
# ```{versionadded} 2.8.1
# ```
#
# [ColReorder](https://datatables.net/extensions/colreorder/) is a DataTables extension
# that lets users drag and drop column headers to reorder the table columns interactively.
#
# Use `colReorder=True` to enable column reordering:

# %% tags=["full-width"]
import itables

itables.init_notebook_mode()

df = itables.sample_dfs.get_countries()

itables.show(df, colReorder=True)

# %% [markdown]
# As always, you can set this option globally with:
# ```python
# itables.options.colReorder = True
# ```
#
# or by adding
# ```
# colReorder = true
# ```
# to your [`itables.toml` configuration file](../configuration.md).
