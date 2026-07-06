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

# Jupyter Widget

The `AgGrid` [Jupyter Widget](https://jupyter.org/widgets) renders your
DataFrames with AG Grid, and lets you read (and set) the selected rows from
Python. It is built on [AnyWidget](https://anywidget.dev). Install it with

```shell
pip install pyaggrid[widget]
```

The `AgGrid` class accepts the same arguments as the `show` function
(but the `df` argument is optional, and `ag_grid_url` is not available
as the widget comes with its own copy of AG Grid):

```{code-cell} ipython3
:tags: [full-width]

import itables_core.sample_dfs
from pyaggrid.widget import AgGrid

df = itables_core.sample_dfs.get_countries()

grid = AgGrid(
    df,
    caption="A DataFrame rendered with the AgGrid widget",
    rowSelection={"mode": "multiRow"},
)
grid
```

## Selected rows

Pass `rowSelection={"mode": "multiRow"}` (or `"singleRow"`) to let the user
select rows. The `selected_rows` attribute of the widget gives you the
indices of the selected rows in the original dataframe (also when the table
is [downsampled](../downsampling.md)), and you can set it from Python:

```{code-cell} ipython3
grid.selected_rows = [0, 2, 5]
```

## Updating the widget

Update the table with the `update` method - here we filter the dataframe
and change the caption:

```{code-cell} ipython3
grid.update(df.head(10), caption="The first 10 countries")
```

## The widget in applications

The `AgGrid` widget works in [Marimo](marimo.md) and, through
[shinywidgets](https://shiny.posit.co/py/docs/jupyter-widgets.html), in
[Shiny](shiny.md) applications - see the example apps at
[`apps/pyaggrid`](https://github.com/mwouts/itables/tree/main/apps/pyaggrid).
