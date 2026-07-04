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

# Select

The [select](https://datatables.net/extensions/select) extension let you select rows (or cells).

~~~{admonition} The `selected_rows` attribute
:class: tip
It is possible to access the `selected_rows` back in Python but for this you will have to use, instead of `show`, either
- the `ITable` [Widget](../apps/widget.md)
- the `ITable` [Dash component](../apps/dash.md)
- the `interactive_table` [Streamlit component](../apps/streamlit.md)

⚠ When a table has been downsampled, only the visible rows can be selected.
~~~

```{tip}
The `select` option also interacts with the [`buttons`](buttons.md) extension. If you click on the CSV or Excel export while having selected some rows, only those rows will be exported - see the example below.
```

```{code-cell} ipython3
import itables

itables.init_notebook_mode()

itables.show(
    itables.sample_dfs.get_countries(),
    select=True,
    selected_rows=[2, 4, 5],
    buttons=["copyHtml5", "csvHtml5", "excelHtml5"],
)
```

```{tip}
The `select` option accept multiple values, as documented [here](https://datatables.net/extensions/select):
- `select=True` or `select="os"` let you select using single click, shift-click and ctrl-click
- `select="single"` let you select a single row
- `select="multi"` for single click selection of multiple rows, `select="multi+shift"`, ...

With `select={"style": "os", "items": "cell"}` you can let the user select specific cells, however the cell selection is not exposed in Python, nor taken into account when exporting the data.
```
