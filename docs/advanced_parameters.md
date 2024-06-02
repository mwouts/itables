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

# Advanced Parameters

ITables is a wrapper for the Javascript [DataTables](https://datatables.net/) library, which has a great [documentation](https://datatables.net/), a huge collection of [examples](https://datatables.net/examples/index), and a useful [forum](https://datatables.net/forums/).

Below we give a series of examples of how the DataTables examples can be ported to Python with `itables`.

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
df = get_countries(html=False)
```

```{code-cell}
:tags: [remove-cell]

import itables.options as opt

opt.lengthMenu = [5, 10, 20, 50, 100, 200, 500]
```

```{tip}
The rocket icon at the top of the page will let you run this notebook in Binder!
```

## Caption

You can set additional `tags` on the table like e.g. a [caption](https://datatables.net/blog/2014-11-07):

```{code-cell}
:tags: [full-width]

show(df, "Countries from the World Bank Database")
```

The caption appears at the bottom of the table by default: this is governed by `caption-side:bottom`
in the [`style` option](style) (but for some reason this is not effective in Jupyter Book 😕).

(layout)=
## Table layout

By default, datatables that don't fit in one page come with a search box, a pagination control, a table summary, etc.
You can select which elements are actually displayed using
DataTables' [`layout` option](https://datatables.net/reference/option/layout) with e.g.:

```{code-cell}
show(df_small, layout={"topStart": "search", "topEnd": None})
```

The available positions are `topStart, topEnd, bottomStart, bottomEnd`. You can also use `top2Start`, etc... (see more
in the [DataTables documentation](https://datatables.net/reference/option/layout)).

Like for the other arguments of `show`, you can change the default value of the dom option with e.g.:

```
import itables.options as opt

opt.layout =  {
    "topStart": "pageLength",
    "topEnd": "search",
    "bottomStart": "info",
    "bottomEnd": "paging"
}  # (default value)
```

```{tip}
The `layout` option was introduced with `itables==2.0` and `DataTables==2.0`
and deprecates the former [`dom` option](https://datatables.net/reference/option/dom).
If you wish to continue using the `dom` option, set `opt.warn_on_dom = False`.
```

## Search

The [search option](https://datatables.net/reference/option/search) let you control the initial value for the search field, and whether the query should be treated as a regular expression or not:

```{code-cell}
show(df, search={"regex": True, "caseInsensitive": True, "search": "s.ain"})
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

Since ITables 2.1.2, the `.dt-layout-table` div has a default overflow equal to `auto`, so in most cases you won't need to use the `scrollX` option of datatables.

## Footer

Use `footer = True` if you wish to display a table footer.

```{code-cell}
:tags: [full-width]

show(df, footer=True)
```

## Column filters

Use `column_filters = "header"` or `"footer"` if you wish to display individual column filters
(remove the global search box with a [`layout`](layout) modifier if desired).

```{code-cell}
alpha_numeric_df = pd.DataFrame(
    [["one", 1.5], ["two", 2.3]], columns=["string", "numeric"]
)

show(alpha_numeric_df, column_filters="footer", layout={"topEnd": None})
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

## Row order

Since `itables>=1.3.0`, the interactive datatable shows the rows in the same order as the original dataframe:

```{code-cell}
from itables.sample_dfs import get_dict_of_test_dfs

for name, test_df in get_dict_of_test_dfs().items():
    if "sorted" in name:
        show(test_df, tags=f"<caption>{name}</caption>".replace("_", " ").title())
```

You can also set an explicit [`order`](https://datatables.net/reference/option/order) argument:

```{code-cell}
sorted_df = pd.DataFrame({"i": [1, 2], "a": [2, 1]}).set_index(["i"])
show(sorted_df, order=[[1, "asc"]])
```

## Showing the index

By default, the index of a Series/DataFrame is shown only when it is not trivial, i.e. when
it has a name, or when it differs from a range index. If you prefer, you can change the value of
`showIndex` to either `True` or `False` to always or never show the index (the default value being `"auto"`).

You can change this behavior globally with e.g.
```python
import itables.options as opt

opt.showIndex = True
```

or locally by passing an argument `showIndex` to the `show` function:

```{code-cell}
df_with_range_index = pd.DataFrame({"letter": list("abcd")})
show(df_with_range_index, showIndex=True)
```
