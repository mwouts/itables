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
# # PyAgGrid: Python DataFrames as interactive AG Grid tables
#
# [![CI](https://github.com/mwouts/itables/actions/workflows/continuous-integration.yml/badge.svg?branch=main)](https://github.com/mwouts/itables/actions)
# [![MIT License](https://img.shields.io/github/license/mwouts/itables)](https://github.com/mwouts/itables/blob/main/LICENSE)
# <a class="github-button" href="https://github.com/mwouts/itables" data-icon="octicon-star" data-show-count="true"></a>
# <script src="https://buttons.github.io/buttons.js"></script>
#
# The `pyaggrid` package renders your Pandas and Polars DataFrames (and more,
# through [Narwhals](https://narwhals-dev.github.io/narwhals/)) as interactive
# [AG Grid](https://www.ag-grid.com/) tables.
#
# `pyaggrid` is developed in the [ITables](https://github.com/mwouts/itables)
# project, together with [`pydatatables`](../pydatatables/index.html) - the
# [DataTables](https://datatables.net/) renderer. The two packages share
# their core functions ([downsampling](downsampling.html), value
# formatting) through the `itables_core` package, and accept the same
# dataframes and the same `maxBytes`/`maxRows`/`maxColumns`/`showIndex`
# arguments - but the tables are rendered with AG Grid, with the AG Grid
# look and [options](https://www.ag-grid.com/javascript-data-grid/grid-options/).
#
# ## Installation
#
# Install `pyaggrid` with
#
# ```shell
# pip install pyaggrid
# ```
#
# ## Quick start
#
# Activate the AG Grid representation for all your DataFrames with

# %%
import pyaggrid

pyaggrid.init_notebook_mode()

# %% [markdown]
# after which every Pandas or Polars DataFrame or Series is rendered as an
# AG Grid table:

# %% tags=["full-width"]
import itables_core.sample_dfs

df = itables_core.sample_dfs.get_countries()
df

# %% [markdown]
# If you prefer to render only selected DataFrames with AG Grid, call
# `pyaggrid.init_notebook_mode(all_interactive=False)` and use `pyaggrid.show`:

# %%
pyaggrid.init_notebook_mode(all_interactive=False)

# %% [markdown]
# By default, the width of the grid container adjusts to the table content
# after the first rendering, so the table is not wider than its columns.
# Set `domLayout="normal"` and a `style` with an explicit size if you prefer
# to control the container size yourself.
#
# ## Themes
#
# AG Grid comes with four built-in themes: `quartz` (the default), `balham`,
# `material` and `alpine`:

# %% tags=["full-width"]
pyaggrid.show(df, theme="balham")

# %% [markdown]
# ## AG Grid options
#
# The `show` and `to_html_aggrid` functions accept the
# [AG Grid options](https://www.ag-grid.com/javascript-data-grid/grid-options/).
# For instance, you can activate row selection and a quick filter:

# %% tags=["full-width"]
pyaggrid.show(
    df,
    rowSelection={"mode": "multiRow"},
    quickFilterText="france",
)

# %% [markdown]
# JavaScript callbacks can be passed using `JavascriptFunction`:

# %% tags=["full-width"]
from pyaggrid import JavascriptFunction

pyaggrid.show(
    df,
    getRowStyle=JavascriptFunction(
        "function (params) { return params.data.c1.startsWith('Europe') ? {background: '#eaf3ff'} : null; }"
    ),
)

# %% [markdown]
# Note that the rows passed to AG Grid are objects with positional keys
# `c0`, `c1`, ... (so that duplicated, non-string, or dotted column names
# cannot confuse AG Grid) - the actual column name is in the `headerName`
# of the generated column definitions. If you pass your own `columnDefs`,
# use e.g. `{"field": "c0", "headerName": "my column"}` to reference the
# first column.
#
# ## Default options
#
# The default values of the options can be changed in `pyaggrid.options`, e.g.

# %%
pyaggrid.options.theme = "quartz"
pyaggrid.options.maxBytes = "128KB"

# %% [markdown]
# The pyaggrid-specific options are documented in
# `pyaggrid.typing.PyAgGridOptions`: `theme`, `showIndex`, `maxBytes`,
# `maxRows`, `maxColumns`, `table_id`, `ag_grid_url`, `classes`, `style`, ...

# %% tags=["remove-cell"]
pyaggrid.options.maxBytes = "64KB"

# %% [markdown]
# ## Downsampling
#
# Like with `pydatatables`, large tables are
# [downsampled](downsampling.html) before being rendered, and a message
# is displayed below the table:

# %% tags=["full-width"]
import numpy as np
import pandas as pd

wide_df = pd.DataFrame(np.random.normal(size=(1000, 100)))
pyaggrid.show(wide_df)

# %% [markdown]
# ## PyAgGrid in applications
#
# PyAgGrid is also available as
# - a [Jupyter Widget](apps/widget.md) (which also works in [Marimo](apps/marimo.md)
#   and [Shiny](apps/shiny.md))
# - a [Dash](apps/dash.md) component
# - a [Streamlit](apps/streamlit.md) component.
#
# The corresponding example apps are at
# [`apps/pyaggrid`](https://github.com/mwouts/itables/tree/main/apps/pyaggrid).
# Unlike `show`, the components come with their own copy of AG Grid, so they
# work offline.
#
# ## Current limitations
#
# Compared to [`pydatatables`](../pydatatables/index.html), the `pyaggrid` package does
# not yet offer:
#
# - an offline mode for `show` and `to_html_aggrid`: AG Grid Community is
#   loaded from the URL set in `pyaggrid.options.ag_grid_url` (jsDelivr by
#   default). The widget, Dash and Streamlit components are not affected -
#   they come with their own copy of AG Grid
# - the [pandas style](../pydatatables/pandas_style.html) support or the export
#   [buttons](../pydatatables/options/buttons.html) of DataTables (AG Grid Community has
#   its own per-column filters and CSV export)
#
# If you need one of these, use [`pydatatables`](../pydatatables/index.html), or open an
# issue at [ITables](https://github.com/mwouts/itables/issues) to let us know!
#
# ## Licence
#
# PyAgGrid is developed by [Marc Wouts](https://github.com/mwouts) on
# [GitHub](https://github.com/mwouts/itables), under an MIT license.
#
# PyAgGrid uses [AG Grid Community](https://github.com/ag-grid/ag-grid),
# which is developed by AG Grid Ltd under an MIT license.
