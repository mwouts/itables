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
# # Classes
#
# Select how your table looks like with the `classes` argument (defaults to `"display nowrap"`) of the `show` function, or by changing `itables.options.classes`.
#
# Add `"compact"` if you want a denser table:

# %% tags=["full-width"]
import itables

itables.init_notebook_mode()

df = itables.sample_dfs.get_countries()

itables.show(df, classes="display nowrap compact")

# %% [markdown]
# Remove `"nowrap"` if you want the cell content to be wrapped:

# %% tags=["full-width"]
itables.show(df, classes="display")

# %% [markdown]
# [More options](https://datatables.net/manual/styling/classes#Table-classes) like `"cell-border"` are available:

# %% tags=["full-width"]
itables.show(df, classes="display nowrap cell-border")
