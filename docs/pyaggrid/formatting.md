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

# Cell Formatting

## Numbers

Float and integer values are passed to AG Grid as numbers, so they are
sorted and filtered numerically. To format them, use a
[`valueFormatter`](https://www.ag-grid.com/javascript-data-grid/value-formatters/),
either in your own `columnDefs`, or for all the columns through
`defaultColDef`:

```{code-cell} ipython3
import math

import pandas as pd

import pyaggrid
from pyaggrid import JavascriptFunction
```

```{code-cell} ipython3
pyaggrid.show(
    pd.DataFrame(
        {"int": range(1, 6), "float": [i * math.pi * 1e4 for i in range(1, 6)]}
    ),
    columnDefs=[
        {"field": "c0", "headerName": "int", "type": "rightAligned"},
        {
            "field": "c1",
            "headerName": "float",
            "type": "rightAligned",
            "valueFormatter": JavascriptFunction(
                "function (params) { return params.value == null ? '' : '$' + params.value.toLocaleString('en-US', {maximumFractionDigits: 3}); }"
            ),
        },
    ],
)
```

Note that the rows passed to AG Grid are objects with positional keys `c0`, `c1`, ...
so when you pass your own `columnDefs` (which replace the generated ones),
use `"field": "c0"` to reference the first column.

## Dates and other types

The non-numeric values (dates, timedeltas, objects...) are formatted in
Python, using the same functions as `pydatatables`: Pandas Series are
formatted with `pandas.io.formats.format.format_array`, and Polars Series
with the Polars native formatting.

```{code-cell} ipython3
pyaggrid.show(pd.DataFrame({"date": pd.date_range("2026-01-01", periods=5, freq="D")}))
```

## Colors based on cell values

You can use Javascript callbacks to set the cell or row style depending on the cell content. For instance, AG Grid's
[`cellStyle`](https://www.ag-grid.com/javascript-data-grid/cell-styles/)
option can be set for every column through `defaultColDef`.

Note how the Javascript callback is declared as a `JavascriptFunction` object below.

```{code-cell} ipython3
pyaggrid.show(
    pd.DataFrame([[-1, 2, -3, 4.0, -5], [6, -7.0, 8, -9.0, 10]], columns=list("abcde")),
    defaultColDef={
        "cellStyle": JavascriptFunction(
            "function (params) { return params.value < 0 ? {color: 'red'} : null; }"
        )
    },
)
```

## Pandas Style

Unlike `pydatatables`, `pyaggrid` cannot render
[Pandas Style](https://pandas.pydata.org/docs/user_guide/style.html)
objects. If you need them, use
[`pydatatables`](../../pandas_style.html).
