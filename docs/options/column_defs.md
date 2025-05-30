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

# Column Definitions

The [`columnDefs.width`](https://datatables.net/reference/option/columns.width) argument let you adjust the column widths.

Note that the default value of `style`, or of `autoWidth` (defaults to `True`), might override custom column widths,
so you might have to change their values as in the examples below.

You can set a fixed width for all the columns with `"targets": "_all"`:

```{code-cell} ipython3
:tags: [full-width]

import itables

itables.init_notebook_mode()

df = itables.sample_dfs.get_countries(html=False)

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

You can use the DataTables [cell classes](https://datatables.net/manual/styling/classes#Cell-classes) like `dt-left`, `dt-center`, `dt-right` etc. to set the cell alignment. Specify it for one table by using the `columnDefs` argument of `show`

```{code-cell} ipython3
:tags: [full-width]

itables.show(df, columnDefs=[{"className": "dt-center", "targets": "_all"}])
```

or globally by setting `itables.options.columnDefs`:

```{code-cell} ipython3
:tags: [full-width]

itables.options.columnDefs = [{"className": "dt-center", "targets": "_all"}]

df
```
