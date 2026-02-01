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
```

# Cell Formatting

## Formatting with Pandas

By default, ITables format floats using Pandas itself, so
you can use [Pandas' formatting options](https://pandas.pydata.org/pandas-docs/stable/user_guide/options.html).

For instance, you can change the precision used to display floating numbers:

```{code-cell} ipython3
import math

import itables

itables.init_notebook_mode()
```

```{code-cell} ipython3
import pandas as pd

with pd.option_context("display.float_format", "{:,.2f}".format):
    itables.show(pd.Series([i * math.pi for i in range(1, 6)]))
```

Or you can use a custom formatter:

```{code-cell} ipython3
with pd.option_context("display.float_format", "${:,.2f}".format):
    itables.show(pd.Series([i * math.pi for i in range(1, 6)]))
```

## Formatting with Polars

By default, ITables v2.7.0 and above formats floats in Polars DataFrames according to the Polars configuration:

```{code-cell} ipython3
import polars as pl

with pl.Config(float_precision=2):
    itables.show(pl.Series([i * math.pi for i in range(1, 6)]))
```

## Formatting with Javascript

If you pass a `columnDefs` argument, the columns that appear in the targets are not formatted - instead they are passed verbatim to datatables.net. Therefore, to achieve a particular formatting you can resort to the
[`columns.render` option](https://datatables.net/examples/advanced_init/column_render.html)
of DataTables.

For instance, this [example](https://datatables.net/forums/discussion/61407/how-to-apply-a-numeric-format-to-a-column)
can be ported like this:

```{code-cell} ipython3
itables.show(
    pd.DataFrame(
        {"int": range(1, 6), "float": [i * math.pi * 1e4 for i in range(1, 6)]}
    ),
    columnDefs=[
        {
            "targets": [1],
            "render": itables.JavascriptCode(
                "$.fn.dataTable.render.number(',', '.', 3, '$')"
            ),
        }
    ],
)
```

## Colors based on cell values

You can use Javascript callbacks to set the cell or row style depending on the cell content.

The example below, in which we color in red the cells with negative numbers, is directly inspired by the corresponding DataTables [example](https://datatables.net/reference/option/columns.createdCell).

Note how the Javascript callback is declared as `JavascriptFunction` object below.

```{code-cell} ipython3
itables.show(
    pd.DataFrame([[-1, 2, -3, 4.0, -5], [6, -7.0, 8, -9.0, 10]], columns=list("abcde")),
    columnDefs=[
        {
            "targets": "_all",
            "createdCell": itables.JavascriptFunction(
                """
function (td, cellData, rowData, row, col) {
    // cellData for floats contains their display (=formatted) value,
    // we need the rawValue from the sort field instead.
    const rawValue = this.api()
        .cell(row, col)
        .render('sort');
    if (rawValue < 0) {
        $(td).css('color', 'red')
    }
}
"""
            ),
        }
    ],
)
```

## Formatting with Pandas style

ITables in version 1.6 and above can render
[Pandas Style](https://pandas.pydata.org/docs/user_guide/style.html)
objects as interactive DataTables.

This way, you can easily add background color, and even
tooltips to your dataframes, and still get them
displayed using DataTables - see our [examples](pandas_style.md).

```{warning}
Please note that Pandas Style objects are rendered using
their `.to_html()` method, which is less efficient that
the default JS data export used by ITables.
```
