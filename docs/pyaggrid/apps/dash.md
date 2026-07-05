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

# Dash

The `AgGrid` [Dash](https://dash.plotly.com/) component renders your
DataFrames with AG Grid in Dash applications. Install it with

```shell
pip install pyaggrid[dash]
```

If you wish to display a DataFrame whose content is fixed (not reacting to the other controls in the application), you just need to import `AgGrid` from `pyaggrid.dash` and add it to your layout like here:

```{include} ../../../apps/pyaggrid/dash/1_display_only.py
:code: python
```

## Selected rows

Listening to the selected rows is simply done by adding
`rowSelection={"mode": "multiRow"}` to the `AgGrid` call, and then
implementing a callback on `Input("my_dataframe", "selected_rows")`:

```{include} ../../../apps/pyaggrid/dash/2_selected_rows.py
:code: python
```

## Updating the component

The `AgGrid` component properties (table content, selected rows, etc.) need
to be updated in a consistent way. We recommend that you list the outputs
with `PyAgGridOutputs("my_dataframe")` in your callback, and update them with
`updated_aggrid_outputs`, which takes the same arguments as `show` plus
`df`, `caption`, `selected_rows` and `current_grid_args`:

```python
from pyaggrid.dash import AgGrid, PyAgGridOutputs, updated_aggrid_outputs

# (...)

@callback(
    PyAgGridOutputs("my_dataframe"),
    [
        Input("caption", "value"),
        State("my_dataframe", "selected_rows"),
        State("my_dataframe", "grid_args"),
    ],
)
def update_table(caption, selected_rows, grid_args):
    return updated_aggrid_outputs(
        caption=caption, selected_rows=selected_rows, current_grid_args=grid_args
    )
```

```{tip}
See also the official [dash-ag-grid](https://dash.plotly.com/dash-ag-grid)
package maintained by Plotly, and the `DataTable` component of
[`pydatatables`](../../pydatatables/apps/dash.html) for the DataTables look.
```
