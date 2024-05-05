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

# Formatting

## Formatting with Pandas

`itables` builds the HTML representation of your Pandas dataframes using Pandas itself, so
you can use [Pandas' formatting options](https://pandas.pydata.org/pandas-docs/stable/user_guide/options.html).
For instance, you can change the precision used to display floating numbers:

```{code-cell}
from itables import init_notebook_mode, show
from itables.sample_dfs import get_countries

init_notebook_mode(all_interactive=True)
```

```{code-cell}
import math

import pandas as pd

with pd.option_context("display.float_format", "{:,.2f}".format):
    show(pd.Series([i * math.pi for i in range(1, 6)]))
```

Or you can use a custom formatter:

```{code-cell}
with pd.option_context("display.float_format", "${:,.2f}".format):
    show(pd.Series([i * math.pi for i in range(1, 6)]))
```

## Formatting with Javascript

Numbers are formatted using Pandas, then are converted back to float to ensure they come in the right order when sorted.
Therefore, to achieve a particular formatting you might have to resort to the
[`columns.render` option](https://datatables.net/examples/advanced_init/column_render.html)
of DataTables.

For instance, this [example](https://datatables.net/forums/discussion/61407/how-to-apply-a-numeric-format-to-a-column)
can be ported like this:

```{code-cell}
from itables import JavascriptCode

show(
    pd.Series([i * math.pi * 1e4 for i in range(1, 6)]),
    columnDefs=[
        {
            "targets": "_all",
            "render": JavascriptCode("$.fn.dataTable.render.number(',', '.', 3, '$')"),
        }
    ],
)
```

## Colors based on cell values

You can use Javascript callbacks to set the cell or row style depending on the cell content.

The example below, in which we color in red the cells with negative numbers, is directly inspired by the corresponding DataTables [example](https://datatables.net/reference/option/columns.createdCell).

Note how the Javascript callback is declared as `JavascriptFunction` object below.

```{code-cell}
from itables import JavascriptFunction

show(
    pd.DataFrame([[-1, 2, -3, 4, -5], [6, -7, 8, -9, 10]], columns=list("abcde")),
    columnDefs=[
        {
            "targets": "_all",
            "createdCell": JavascriptFunction(
                """
function (td, cellData, rowData, row, col) {
    if (cellData < 0) {
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

## HTML in cells

### A simple example

HTML content is supported, which means that you can have formatted text,
links or even images in your tables:

```{code-cell}
pd.Series(
    [
        "<b>bold</b>",
        "<i>italic</i>",
        '<a href="https://github.com/mwouts/itables">link</a>',
    ],
    name="HTML",
)
```

### Images in a table

```{code-cell}
:tags: [full-width]

df = get_countries(html=False)

df["flag"] = [
    '<a href="https://flagpedia.net/{code}">'
    '<img src="https://flagpedia.net/data/flags/h80/{code}.webp" '
    'alt="Flag of {country}"></a>'.format(code=code.lower(), country=country)
    for code, country in zip(df.index, df["country"])
]
df["country"] = [
    '<a href="https://en.wikipedia.org/wiki/{}">{}</a>'.format(country, country)
    for country in df["country"]
]
df["capital"] = [
    '<a href="https://en.wikipedia.org/wiki/{}">{}</a>'.format(capital, capital)
    for capital in df["capital"]
]
df
```

### Base64 images

[Base64 encoded image](https://stackoverflow.com/a/8499716/9817073) are supported, too:

```{code-cell}
pd.Series(
    {
        "url": '<img src="https://storage.googleapis.com/tfds-data/visualization/fig/mnist-3.0.1.png" height="50" alt="MNIST">',
        "base64": '<img src="data:image/png;base64, iVBORw0KGgoAAAANSUhEUgAAAAUA'
        "AAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO"
        '9TXL0Y4OHwAAAABJRU5ErkJggg==" alt="Red dot">',
    },
    name="Images",
)
```
