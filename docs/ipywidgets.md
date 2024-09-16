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

# Jupyter Widget

ITables is available as a [Jupyter Widget](https://ipywidgets.readthedocs.io) since v2.2.

## Using `show`

If you only want to _display_ the table, you **do not need**
our Jupyter widget. The `show` function is enough!

```{code-cell}
import ipywidgets as widgets

from itables import show
from itables.sample_dfs import get_dict_of_test_dfs

sample_dfs = get_dict_of_test_dfs()


def use_show_in_interactive_output(table_name: str):
    show(
        sample_dfs[table_name],
        caption=table_name,
        style="table-layout:auto;width:auto;float:left;caption-side:bottom",
    )


table_selector = widgets.Dropdown(options=sample_dfs.keys(), value="int_float_str")
out = widgets.interactive_output(
    use_show_in_interactive_output, {"table_name": table_selector}
)

widgets.VBox([table_selector, out])
```

```{tip}
Jupyter widgets only work in a live notebook.
Click on the rocket icon at the top of the page to run this demo in Binder.
```

## Using the ITable widget

The `ITable` widget has a few dependencies that you can install with
```bash
pip install itables[widget]
```

The `ITable` class accepts the same arguments as the `show` method, but
the `df` argument is optional.

```{code-cell}
from itables.widget import ITable

table = ITable(selected_rows=[0, 2, 5, 99])


def update_selected_table(change):
    table_name = table_selector.value
    table.update(
        sample_dfs[table_name],
        caption=table_name,
        select=True,
        style="table-layout:auto;width:auto;float:left",
    )


# Update the table when the selector changes
table_selector.observe(update_selected_table, "value")

# Set the table to the initial table selected
update_selected_table(None)

widgets.VBox([table_selector, table])
```

## Get the selected rows

The `ITable` widget let you access the state of the table
and in particular, it has an `.selected_rows` attribute
that you can use to determine the rows that have been
selected by the user (allow selection by passing `select=True`
to the `ITable` widget).

```{code-cell}
out = widgets.Output()


def show_selected_rows(change):
    with out:
        out.clear_output()
        print("selected_rows: ", table.selected_rows)


table.observe(show_selected_rows, "selected_rows")

# Display the initial selection
show_selected_rows(None)

out
```

## Limitations

Compared to `show`, the `ITable` widget has the same limitations as the [streamlit component](streamlit.md#limitations),
e.g. structured headers are not available, you can't pass JavaScript callback, etc.
