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

# Table Style and CSS

As usual, we initialize ITables with `init_notebook_mode`, and we create two sample DataFrames:

```{code-cell} ipython3
:tags: [hide-input]

import pandas as pd

import itables

df = itables.sample_dfs.get_countries(html=False)
df_small = pd.DataFrame({"a": [2, 1]})

itables.init_notebook_mode()
```

## Classes

Select how your table looks like with the `classes` argument (defaults to `"display nowrap"`) of the `show` function, or by changing `itables.options.classes`.

Add `"compact"` if you want a denser table:

```{code-cell} ipython3
:tags: [full-width]

itables.show(df, classes="display nowrap compact")
```

Remove `"nowrap"` if you want the cell content to be wrapped:

```{code-cell} ipython3
:tags: [full-width]

itables.show(df, classes="display")
```

[More options](https://datatables.net/manual/styling/classes#Table-classes) like `"cell-border"` are available:

```{code-cell} ipython3
:tags: [full-width]

itables.show(df, classes="display nowrap cell-border")
```

## CSS

You can use CSS to alter how the interactive DataTables are rendered.

For instance, we change the
[font size](https://developer.mozilla.org/en-US/docs/Web/CSS/font-size)
for all the tables in the document with this code:

```{code-cell} ipython3
from IPython.display import HTML, display

css = """
.dt-container {
  font-size: small;
}
"""
display(HTML(f"<style>{css}</style>" ""))
```

This is helpful for instance in the context of
[Quarto presentations](quarto.md).

With this over CSS, we change _every datatable_ table header
in the notebook to bold/italic.

```{code-cell} ipython3
css = """
.dataTable th {
    font-weight: bolder;
    font-style: italic;
}
"""
display(HTML(f"<style>{css}</style>" ""))
```

You might also want to alter the style of specific tables only.
To do this, add a new class to the target tables, as
in the example below:

```{code-cell} ipython3
class_specific_css = ".table_with_monospace_font { font-family: courier, monospace }"
display(HTML(f"<style>{class_specific_css}</style>" ""))
```

```{code-cell} ipython3
itables.show(df, classes="display nowrap table_with_monospace_font")
```

(style)=
## The style argument

The `show` function has a `style` argument that determines the
style for that particular table.

The default value for `style` is `"table-layout:auto;width:auto;margin:auto;caption-side:bottom"`.
Without `width:auto`, tables with few columns are stretched to fit the container width.
Using `margin:auto` makes non-wide tables centered.

## Position and width

You can set a specific width or position for a table using with the `style` argument of the show function:

```{code-cell} ipython3
itables.show(df_small, style="table-layout:auto;width:50%;float:right")
```

or you can also change it for all tables by changing `itables.options.style`:

```python
itables.options.style = "table-layout:auto;width:auto"
```

```{tip}
For ajusting the height of a table, see the section on [pagination](advanced_parameters.md#pagination).
```

## Column width

The [`columnDefs.width`](https://datatables.net/reference/option/columns.width) argument let you adjust the column widths.

Note that the default value of `style`, or of `autoWidth` (defaults to `True`), might override custom column widths,
so you might have to change their values as in the examples below.

You can set a fixed width for all the columns with `"targets": "_all"`:

```{code-cell} ipython3
:tags: [full-width]

itables.show(
    df,
    columnDefs=[{"width": "120px", "targets": "_all"}],
    style="width:1200px",
    autoWidth=False,
)
```

You can also adjust the width of selected columns only:

```{code-cell} ipython3
:tags: [full-width]

itables.show(
    df,
    columnDefs=[{"width": "30%", "targets": [2, 3]}],
    style="width:100%;margin:auto",
)
```

If you wish you can also set a value for `columnDefs` permanently in `itables.options` as demonstrated in the cell alignment example below.

## Cell alignment

You can use the DataTables [cell classes](https://datatables.net/manual/styling/classes#Cell-classes) like `dt-left`, `dt-center`, `dt-right` etc. to set the cell alignment. Specify it for one table by using the `columnDefs` argument of `show`

```{code-cell} ipython3
itables.show(df, columnDefs=[{"className": "dt-center", "targets": "_all"}])
```

or globally by setting `itables.options.columnDefs`:

```{code-cell} ipython3
itables.options.columnDefs = [{"className": "dt-center", "targets": "_all"}]
df
```
