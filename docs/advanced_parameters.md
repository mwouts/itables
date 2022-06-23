---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.13.8
kernelspec:
  display_name: itables
  language: python
  name: itables
---

# Advanced parameters

The `itables` package is a wrapper for the Javascript [datatables.net](https://datatables.net/) library, which has a great [documentation](https://datatables.net/), a huge collection of [examples](https://datatables.net/examples/index), and a useful [forum](https://datatables.net/forums/).

Below we give a few examples of how the datatables.net examples can be ported to Python with `itables`.

As always, we initialize the `itables` library with

```{code-cell}
from itables import init_notebook_mode, show

init_notebook_mode(all_interactive=True)
```

and we load a sample dataframe

```{code-cell}
from itables.sample_dfs import get_countries

df = get_countries()
```

## Row sorting

Select the order in which the row are sorted with the [datatables' `order`](https://datatables.net/reference/option/order) argument. By default, the rows are sorted according to the first column (`order = [[0, 'asc']]`).

If you want to deactivate the sorting, set `order = []`, either in the `show` method, or as a global option:

```{code-cell}
import pandas as pd
import itables.options as opt

opt.order = []  # no sorting
pd.DataFrame({"a": [2, 1]})
```

## Pagination

### How many rows per page

Select [how many entries](https://datatables.net/examples/advanced_init/length_menu.html) should appear at once in the table with either the `lengthMenu` argument of the `show` function, or with the global option `itables.options.lengthMenu`:

```{code-cell}
import itables.options as opt

opt.lengthMenu = [2, 5, 10, 20, 50, 100, 200, 500]
df
```

### Show the table in full

Show the table in full with the [`paging` argument](https://datatables.net/reference/option/paging), either in the `show` method, or in the options:

```{code-cell}
show(df.head(), paging=False)
```

### Scroll

If you prefer to replace the pagination with a [vertical scroll](https://datatables.net/examples/basic_init/scroll_y.html), use for instance

```{code-cell}
show(df, scrollY="200px", scrollCollapse=True, paging=False)
```

## Table and cell style

Select how your table should look like with the `classes` argument of the `show` function, or by changing `itables.options.classes`. For the list of possible values, see [datatables' default style](https://datatables.net/manual/styling/classes) and [the style examples](https://datatables.net/examples/styling/).

```{code-cell}
opt.classes = ["display", "nowrap"]
df
```

```{code-cell}
opt.classes = ["display", "cell-border"]
df
```

## Table captions

You can set additional `tags` like a [caption](https://datatables.net/blog/2014-11-07) on the table with the `tags` option:

```{code-cell}
show(df, tags="<caption>Countries from the World Bank Database</caption>")
```

The position of the caption can be set explicitly as in the datatables example above (note that the default position may depend on how you render the notebook):

```{code-cell}
show(
    df,
    tags='<caption style="caption-side: top">Countries from the World Bank Database</caption>',
)
```

```{code-cell}
opt.lengthMenu = [5, 10, 20, 50, 100, 200, 500]
```

## Table footer

Use `footer = True` if you wish to display a table footer.

```{code-cell}
show(df, footer=True)
```

## Column filters

Use `column_filters = "header"` or `"footer"` if you wish to display individual column filters
(remove the global search box with [`dom='lrtip'`](https://datatables.net/reference/option/dom) if desired).

```{code-cell}
alpha_numeric_df = pd.DataFrame(
    [["one", 1.5], ["two", 2.3]], columns=["string", "numeric"]
)

show(alpha_numeric_df, column_filters="footer", dom="lrtip")
```

As always you can set activate column filters by default with e.g.

```{code-cell}
opt.column_filters = "footer"
alpha_numeric_df
```

Column filters also work on dataframes with multiindex columns:

```{code-cell}
from itables.sample_dfs import get_dict_of_test_dfs

get_dict_of_test_dfs()["multiindex"]
```

Now we deactivate the column filters for the rest of the notebook

```{code-cell}
opt.column_filters = False
```

## Float precision

Floats are rounded using `pd.options.display.float_format`. Please change that format according to your preference.

```{code-cell}
import math
import pandas as pd

with pd.option_context("display.float_format", "{:,.2f}".format):
    show(pd.Series([i * math.pi for i in range(1, 6)]))
```

You may also choose to convert floating numbers to strings:

```{code-cell}
with pd.option_context("display.float_format", "${:,.2f}".format):
    show(pd.Series([i * math.pi for i in range(1, 6)]))
```

## Advanced cell formatting with JS callbacks

You can use Javascript callbacks to set the cell or row style depending on the cell content.

The example below, in which we color in red the cells with negative numbers, is directly inspired by the corresponding datatables.net [example](https://datatables.net/reference/option/columns.createdCell).

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

## Column width

The [`columnDefs.width`](https://datatables.net/reference/option/columns.width) argument let you adjust the column widths.

You can set a fixed width for all the columns with `"targets": "_all"`:

```{code-cell}
show(
    df,
    columnDefs=[{"width": "120px", "targets": "_all"}],
)
```

You can also adjust the width of selected columns only:

```{code-cell}
show(
    df,
    columnDefs=[{"width": "20%", "targets": [2, 3]}],
)
```

If you wish you can also set a value for `columnDefs` permanently in `itables.options` as demonstrated in the cell alignment example below.

## Cell alignment

You can use the datatables.net [cell classes](https://datatables.net/manual/styling/classes#Cell-classes) like `dt-left`, `dt-center`, `dt-right` etc to set the cell alignment. Specify it for one table by using the `columnDefs` argument of `show`

```{code-cell}
show(df, columnDefs=[{"className": "dt-center", "targets": "_all"}])
```

or globally by setting `opt.columnDefs`:

```{code-cell}
opt.columnDefs = [{"className": "dt-center", "targets": "_all"}]
df
```

```{code-cell}
del opt.columnDefs
```

## HTML in cells

```{code-cell}
import pandas as pd

show(
    pd.Series(
        [
            "<b>bold</b>",
            "<i>italic</i>",
            '<a href="https://github.com/mwouts/itables">link</a>',
        ],
        name="HTML",
    ),
    paging=False,
)
```

## The search option

The [search option](https://datatables.net/reference/option/search) let you control the initial value for the search field, and whether the query should be treated as a regular expression or not:

```{code-cell}
show(df, search={"regex": True, "caseInsensitive": True, "search": "s.ain"})
```

## Select rows

Not currently implemented. May be made available at a later stage using the [select](https://datatables.net/extensions/select/) extension for datatables.

+++

## Copy, CSV, PDF and Excel buttons

Not currently implemented. May be made available at a later stage thanks to the [buttons](https://datatables.net/extensions/buttons/) extension for datatable.
