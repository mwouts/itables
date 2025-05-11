---
jupytext:
  formats: md:myst
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

If you wish to display a DataFrame which content is fixed (not reacting to the other controls in the application), you just need to import `ITable` from `itables.dash` and add it to your layout like here:

```{include} ../../apps/dash/1_display_only.py
:code: python
```

## Selected rows

Listening to the selected rows is simply done by adding `select=True` to the `ITable` call, and then implementing a callback on `Input("my_dataframe", "selected_rows")`.

```{include} ../../apps/dash/2_selected_rows.py
:code: python
```

## Updating the DataFrame

The `ITable` component has many properties. These properties (table content, selected rows etc) need to be updated in a consistent way. Therefore we recommend that you list the outputs with `ITableOutputs("my_dataframe")` in your callback, and update them with `updated_itable_outputs` which takes the same arguments as `show`, e.g. `df`, `caption`, `selected_rows`, etc, like in the below (extracted from this [example app](https://github.com/mwouts/itables/tree/main/apps/dash/3_update_table.py)):

```python
from itables.dash import ITable, ITableOutputs, updated_itable_outputs

# (...)

@callback(
    ITableOutputs("my_dataframe"),
    [
        Input("checklist", "value"),
        Input("caption", "value"),
        State("my_dataframe", "selected_rows"),
        State("my_dataframe", "dt_args"),
    ],
)
def update_table(checklist, caption, selected_rows, dt_args):
    if checklist is None:
        checklist = []

    kwargs = {}

    # When df=None and when the dt_args don't change, the table is not updated
    if callback_context.triggered_id == "checklist":
        kwargs["df"] = get_countries(html="HTML" in checklist)

    kwargs["select"] = "Select" in checklist
    if "Buttons" in checklist:
        kwargs["buttons"] = ["copyHtml5", "csvHtml5", "excelHtml5"]

    return updated_itable_outputs(
        caption=caption, selected_rows=selected_rows, current_dt_args=dt_args, **kwargs
    )
```
