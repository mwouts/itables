---
jupytext:
  formats: docs///md:myst,docs/py///py:percent
  notebook_metadata_filter: -jupytext.text_representation.jupytext_version
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
kernelspec:
  display_name: itables
  language: python
  name: itables
---

```{code-cell} ipython3
:tags: [remove-cell]

# ruff: noqa: E402
# pyright: reportUnusedExpression=false
```

# PyAgGrid

The `pyaggrid` package renders your Pandas and Polars DataFrames (and more,
through [Narwhals](https://narwhals-dev.github.io/narwhals/)) as interactive
[AG Grid](https://www.ag-grid.com/) tables.

It shares its core functions ([downsampling](downsampling.md), value
[formatting](formatting.md)) with `pydatatables` through the `itables_core`
package, so the two renderers accept the same dataframes and the same
`maxBytes`/`maxRows`/`maxColumns`/`showIndex` arguments - but the tables are
rendered with AG Grid, with the AG Grid look and
[options](https://www.ag-grid.com/javascript-data-grid/grid-options/).

## Installation

Install `pyaggrid` with

```shell
pip install pyaggrid
```

## Quick start

Activate the AG Grid representation for all your DataFrames with

```{code-cell} ipython3
import pyaggrid

pyaggrid.init_notebook_mode()
```

after which every Pandas or Polars DataFrame or Series is rendered as an
AG Grid table:

```{code-cell} ipython3
:tags: [full-width]

import pydatatables

df = pydatatables.sample_dfs.get_countries()
df
```

If you prefer to render only selected DataFrames with AG Grid, call
`pyaggrid.init_notebook_mode(all_interactive=False)` and use `pyaggrid.show`:

```{code-cell} ipython3
pyaggrid.init_notebook_mode(all_interactive=False)
```

## Themes

AG Grid comes with four built-in themes: `quartz` (the default), `balham`,
`material` and `alpine`:

```{code-cell} ipython3
:tags: [full-width]

pyaggrid.show(df, theme="balham")
```

## AG Grid options

The `show` and `to_html_aggrid` functions accept the
[AG Grid options](https://www.ag-grid.com/javascript-data-grid/grid-options/).
For instance, you can activate row selection and a quick filter:

```{code-cell} ipython3
:tags: [full-width]

pyaggrid.show(
    df,
    rowSelection={"mode": "multiRow"},
    quickFilterText="france",
)
```

JavaScript callbacks can be passed using `JavascriptFunction`:

```{code-cell} ipython3
:tags: [full-width]

from pyaggrid import JavascriptFunction

pyaggrid.show(
    df,
    getRowStyle=JavascriptFunction(
        "function (params) { return params.data[1].startsWith('Europe') ? {background: '#eaf3ff'} : null; }"
    ),
)
```

Note that the rows passed to AG Grid are arrays, not objects: the generated
column definitions use a `valueGetter` and a `colId` equal to
`"c" + column_index`. If you pass your own `columnDefs`, they replace the
generated ones, so use e.g.
`"valueGetter": JavascriptFunction("function (params) { return params.data[0]; }")`
to access the first column.

## Default options

The default values of the options can be changed in `pyaggrid.options`, e.g.

```{code-cell} ipython3
pyaggrid.options.theme = "quartz"
pyaggrid.options.maxBytes = "128KB"
```

The pyaggrid-specific options are documented in
`pyaggrid.typing.PyAgGridOptions`: `theme`, `showIndex`, `maxBytes`,
`maxRows`, `maxColumns`, `table_id`, `ag_grid_url`, `classes`, `style`, ...

```{code-cell} ipython3
:tags: [remove-cell]

pyaggrid.options.maxBytes = "64KB"
```

## Downsampling

Like with `pydatatables`, large tables are [downsampled](downsampling.md)
before being rendered, and a message is displayed below the table:

```{code-cell} ipython3
:tags: [full-width]

import numpy as np
import pandas as pd

wide_df = pd.DataFrame(np.random.normal(size=(1000, 100)))
pyaggrid.show(wide_df)
```

## Current limitations

Compared to `pydatatables`, the `pyaggrid` package does not yet offer:

- an offline mode: AG Grid Community is loaded from the URL set in
  `pyaggrid.options.ag_grid_url` (jsDelivr by default)
- the Jupyter Widget, [Dash](apps/dash.md), [Streamlit](apps/streamlit.md)
  or [Shiny](apps/shiny.md) components
- the [pandas style](pandas_style.md) support, the
  [column filters](options/column_filters.md), or the export
  [buttons](options/buttons.md) of DataTables (AG Grid Community has its own
  per-column filters and CSV export)

If you need one of these, use [`pydatatables`](quick_start.md), or open an
issue at [ITables](https://github.com/mwouts/itables/issues) to let us know!
