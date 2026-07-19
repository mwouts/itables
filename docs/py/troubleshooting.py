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
# pyright: reportDuplicateImport=false
# pyright: reportUnknownVariableType=false

# %% [markdown]
# # Troubleshooting
#
# ITables tables are interactive, but that requires JavaScript to actually run
# in whatever is displaying the notebook. When it can't, you will see one of
# two things instead: a table stuck on "Loading ITables...", or, since ITables v2.9, a small static
# preview. This page explains both, and how to get the interactive table back
# - when that is possible.
#
# ## Stuck on "Loading ITables..."?

# %% tags=["hide-input"]
import pandas as pd

import itables

df = pd.DataFrame()

itables.show(df, connected=False)

# %% [markdown]
# This means your browser *can* run JavaScript, but the DataTables library
# that ITables relies on was never loaded. The most likely causes are:
# - You forgot to run `init_notebook_mode()` (like in the example above), or
#   you deleted that cell or its output.
# - You ran `init_notebook_mode(connected=True)` but you are not connected to
#   the internet, so the library cannot be fetched.
#
# ```{tip}
# If you change the value of the `connected` argument in
# the `init_notebook_mode` cell, you need to re-execute all the cells
# that display interactive tables.
# ```
#
# (static-preview-instead-of-the-interactive-table)=
# ## Seeing a static preview instead?
#
# If, instead of "Loading...", you see non-interactive table, then
# JavaScript could not run **at all** where that table is being rendered -
# your browser was never given the chance to load anything. In that case, ITables v2.9+ falls back to a **static preview**: a plain HTML (or, when printed
# by `itables.show()` outside of a notebook, Markdown) table with only the
# first rows - 10 by default, or as many as your `pageLength`/`lengthMenu`
# options say. This lets you check the table content, but you can't sort,
# search or paginate it. Here is what that plain HTML table looks like:

# %%
from IPython.display import HTML, display

df = itables.sample_dfs.get_countries()
display(HTML(itables.to_html_static_preview(df)))

# %% [markdown]
# There are two situations where this happens, and only one of them can be
# fixed:
#
# - **You can fix it**: the notebook you're viewing is not _trusted_. This
#   happens when you have not run the notebook in full yourself - e.g. it was
#   sent to you with outputs, or it was created by a tool like `papermill`.
#   Tell Jupyter that you trust it (run "Trust Notebook" in View / Activate
#   Command Palette), and the interactive table will appear.
# - **You can't fix it**: you are looking at a static rendering of the
#   notebook, such as [GitHub's preview](fallbacks/static_preview.md) of an `.ipynb` file.
#   There, JavaScript never runs, no matter how the notebook was created or
#   trusted, so the static preview is all you will ever see on that page. Open
#   the notebook in an actual, JavaScript-capable Jupyter session to get the
#   interactive table. See
#   [static_preview_demo.ipynb](https://github.com/mwouts/itables/blob/main/tests/data/static_preview_notebooks/static_preview_demo.ipynb)
#   for a live example of both.
#
# ## Check ITables' version
#
# If the above does not help, please check out the [ChangeLog](changelog.md)
# and decide whether you should upgrade `itables`. You can tell the version
# of ITables that you are using by looking at the loading message (from ITables v2.0.1 on)
# or by running this code snippet:

# %%
import itables

itables.__version__
