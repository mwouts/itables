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

Then we create two sample dataframes:

```{code-cell}
import pandas as pd
from itables.sample_dfs import get_countries

df_small = pd.DataFrame({"a": [2, 1]})
df = get_countries()
```

## Position and width

The default value for the table CSS is `table-layout:auto;width:auto;margin:auto;caption-side:bottom`.
Without `width:auto`, tables with few columns still take the full notebook width in Jupyter.
Using `margin:auto` makes non-wide tables centered in Jupyter.

You can change the CSS used for a single table with e.g.

```{code-cell}
show(df_small, style="table-layout:auto;width:50%;float:right")
```

or you can also change it for all tables by changing `itables.options.style`:

```python
import itables.options as opt

opt.style = "table-layout:auto;width:auto"
```

```{code-cell}
:tags: [remove-cell]

import itables.options as opt

opt.lengthMenu = [5, 10, 20, 50, 100, 200, 500]
```

## Theme

Select how your table looks like with the `classes` argument (defaults to `"display nowrap"`) of the `show` function, or by changing `itables.options.classes`.

Add `"compact"` if you want a denser table:

```{code-cell}
:tags: [full-width]

show(df, classes="display nowrap compact")
```

Remove `"nowrap"` if you want the cell content to be wrapped:

```{code-cell}
:tags: [full-width]

show(df, classes="display", scrollX=True)
```

[More options](https://datatables.net/manual/styling/classes#Table-classes) like `"cell-border"` are available:

```{code-cell}
:tags: [full-width]

show(df, classes="display nowrap cell-border")
```

## Caption

You can set additional `tags` on the table like e.g. a [caption](https://datatables.net/blog/2014-11-07):

```{code-cell}
:tags: [full-width]

show(df, "Countries from the World Bank Database")
```

The caption appears at the bottom of the table by default. This is governed by `caption-side:bottom`
in the `style` option which you can change. You can also override the location of the caption in the caption tag itself:

```{code-cell}
:tags: [full-width]

show(
    df,
    tags='<caption style="caption-side: top">Countries from the World Bank Database</caption>',
)
```

```{code-cell}
:tags: [remove-input]

opt.lengthMenu = [5, 10, 20, 50, 100, 200, 500]
```

## Removing the search box

By default, datatables comes with a search box, a pagination control, a table summary, etc.
You can select which elements are actually displayed using
DataTables' [`dom` option](https://datatables.net/reference/option/dom) with e.g.:

```{code-cell}
show(df_small, dom="tpr")
```

The available elements are:
- `l`: length changing input control
- `f`: filtering input
- `t`: the table itself
- `i`: table information summary
- `p`: pagination control
- `r`: processing display element

Like for the other arguments of `show`, you can change the default value of the dom option with e.g.:

```{code-cell}
import itables.options as opt

opt.dom = "lfrtip"  # (default value)
```

## Pagination

### How many rows per page

Select [how many entries](https://datatables.net/examples/advanced_init/length_menu.html) should appear at once in the table with either the `lengthMenu` argument of the `show` function, or with the global option `itables.options.lengthMenu`:

```{code-cell}
:tags: [full-width]

show(df, lengthMenu=[2, 5, 10, 20, 50])
```

### Show the table in full

Use [`paging=False`](https://datatables.net/reference/option/paging) to show the table in full:

```{code-cell}
:tags: [full-width]

show(df.head(8), paging=False)
```

### Scroll

You can replace the pagination with a [vertical scroll](https://datatables.net/examples/basic_init/scroll_y.html):

```{code-cell}
:tags: [full-width]

show(df, scrollY="200px", scrollCollapse=True, paging=False)
```

In the context of the notebook, a horizontal scroll bar should appear when the table is too wide. In other contexts like here in Jupyter Book, you might want to use `scrollX = True`.

## Table footer

Use `footer = True` if you wish to display a table footer.

```{code-cell}
:tags: [full-width]

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
```

Column filters also work on dataframes with multiindex columns:

```{code-cell}
from itables.sample_dfs import get_dict_of_test_dfs

get_dict_of_test_dfs()["multiindex"]
```

```{code-cell}
:tags: [remove-cell]

opt.column_filters = False
```

## Pandas formatting

`itables` builds the HTML representation of your Pandas dataframes using Pandas itself, so
you can use [Pandas' formatting options](https://pandas.pydata.org/pandas-docs/stable/user_guide/options.html).
For instance, you can change the precision used to display floating numbers:

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

## Row order

Since `itables>=1.3.0`, the interactive datatable shows the rows in the same order as the original dataframe:

```{code-cell}
from itables.sample_dfs import get_dict_of_test_dfs

for name, test_df in get_dict_of_test_dfs().items():
    if "sorted" in name:
        show(
            test_df,
            tags=f"<caption>{name}</caption>".replace("_", " ").title(),
            dom="tpr",
        )
```

You can also set an explicit [`order`](https://datatables.net/reference/option/order) argument:

```{code-cell}
sorted_df = pd.DataFrame({"i": [1, 2], "a": [2, 1]}).set_index(["i"])
show(sorted_df, order=[[1, "asc"]], dom="tpr")
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
:tags: [full-width]

show(df, columnDefs=[{"width": "120px", "targets": "_all"}], scrollX=True)
```

You can also adjust the width of selected columns only:

```{code-cell}
:tags: [full-width]

show(
    df,
    columnDefs=[{"width": "30%", "targets": [2, 3]}],
)
```

If you wish you can also set a value for `columnDefs` permanently in `itables.options` as demonstrated in the cell alignment example below.

## Cell alignment

You can use the datatables.net [cell classes](https://datatables.net/manual/styling/classes#Cell-classes) like `dt-left`, `dt-center`, `dt-right` etc. to set the cell alignment. Specify it for one table by using the `columnDefs` argument of `show`

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
