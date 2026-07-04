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
# # Notebook Mode
#
# Activate PyAgGrid in a Jupyter environment for all your tables with `init_notebook_mode`:

# %%
import pyaggrid

pyaggrid.init_notebook_mode()

# %% [markdown]
# You can go back to the standard HTML representation of Pandas DataFrames with `init_notebook_mode(all_interactive=False)`.

# %% tags=["full-width"]
import itables_core.sample_dfs

df = itables_core.sample_dfs.get_countries()
df

# %% [markdown]
# ```{warning}
# Unlike `pydatatables`, `pyaggrid` does not have an offline mode yet:
# the AG Grid library is loaded from the URL set in
# `pyaggrid.options.ag_grid_url` (jsDelivr by default), so an internet
# connection is required when the tables are displayed.
# ```
#
# ## Show
#
# If you prefer to render only certain tables using `pyaggrid`, or want to set additional options, use `show`:

# %% tags=["full-width"]
pyaggrid.show(df, caption="A DataFrame rendered with PyAgGrid")
