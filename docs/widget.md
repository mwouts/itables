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

## The `ITable` widget

The `ITable` widget has a few dependencies (essentially [AnyWidget](https://anywidget.dev),
a great widget development framework!) that you can install with
```bash
pip install itables[widget]
```

The `ITable` class accepts the same arguments as the `show` method, but
the `df` argument is optional.

```{code-cell}
from itables.sample_dfs import get_dict_of_test_dfs
from itables.widget import ITable

df = get_dict_of_test_dfs()["int_float_str"]

table = ITable(df, selected_rows=[0, 2, 5], select=True)
table
```

```{tip}
The table shown above does not reflect the initial row selection.
This is because the `ITable` widget was updated with
more row selection commands, see below.
```

## The `selected_rows` traits

The `selected_rows` attribute of the `ITable` object provides a view on the
rows that have been selected in the table (remember to pass [`select=True`](select.md)
to activate the row selection). You can use it to either retrieve
or change the current row selection:

```{code-cell}
table.selected_rows
```

```{code-cell}
table.selected_rows = [3, 4]
```

## The `df` property

Use it to retrieve the table data:

```{code-cell}
table.df.iloc[table.selected_rows]
```

or to update it

```{code-cell}
table.df = df.head(6)
```

```{tip}
`ITable` will raise an `IndexError` if the `selected_rows` are not consistent with the
updated data. If you need to update the two simultaneously, use `table.update(df, selected_rows=...)`, see below.
```

## The `caption`, `style` and `classes` traits

You can update these traits from Python, e.g.

```{code-cell}
table.caption = "numbers and strings"
```

## The `update` method

Last but not least, you can update the `ITable` arguments simultaneously using the `update` method:

```{code-cell}
table.update(df.head(20), selected_rows=[7, 8])
```

## Limitations

Compared to `show`, the `ITable` widget has the same limitations as the [Streamlit component](streamlit.md#limitations),
e.g. structured headers are not available, you can't pass JavaScript callback, etc.

The good news is that if you only want to _display_ the table, you do not need
the `ITable` widget. Below is an example in which we use `show` to display a different
table depending on the value of a drop-down component:

```python
import ipywidgets as widgets
from itables import show
from itables.sample_dfs import get_dict_of_test_dfs

def use_show_in_interactive_output(table_name: str):
    show(
        sample_dfs[table_name],
        caption=table_name,
    )

sample_dfs = get_dict_of_test_dfs()
table_selector = widgets.Dropdown(options=sample_dfs.keys(), value="int_float_str")

out = widgets.interactive_output(
    use_show_in_interactive_output, {"table_name": table_selector}
)

widgets.VBox([table_selector, out])
```
