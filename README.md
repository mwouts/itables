# Pandas DataFrames and Series as Interactive DataTables

[![Pypi](https://img.shields.io/pypi/v/itables.svg)](https://pypi.python.org/pypi/itables)
![CI](https://github.com/mwouts/itables/workflows/CI/badge.svg)
[![codecov.io](https://codecov.io/github/mwouts/itables/coverage.svg?branch=main)](https://codecov.io/github/mwouts/itables?branch=main)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/mwouts/itables.svg)](https://lgtm.com/projects/g/mwouts/itables/context:python)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Notebook](https://img.shields.io/badge/Binder-Notebook-blue.svg)](https://mybinder.org/v2/gh/mwouts/itables/main?filepath=README.md)
[![Lab](https://img.shields.io/badge/Binder-JupyterLab-blue.svg)](https://mybinder.org/v2/gh/mwouts/itables/main?urlpath=lab/tree/README.md)
<a class="github-button" href="https://github.com/mwouts/itables" data-icon="octicon-star" data-show-count="true" aria-label="Star mwouts/itables on GitHub">Star</a>

Turn pandas DataFrames and Series into interactive [datatables](https://datatables.net) in your notebooks!

![](https://raw.githubusercontent.com/mwouts/itables/main/demo/itables.gif)

# Quick start

Install the package with

```
pip install itables
```

Activate the interactive mode for all series and dataframes with

```python
from itables import init_notebook_mode
init_notebook_mode(all_interactive=True)
```

Then any dataframe will be displayed as an interactive [datatables](https://datatables.net) table:

```python
import world_bank_data as wb

df = wb.get_countries()
df
```

If you want to display just one series or dataframe as an interactive table, use `itables.show`:

```python
from itables import show

x = wb.get_series("SP.POP.TOTL", mrv=1, simplify_index=True)
show(x)
```

(NB: In Jupyter Notebook and Jupyter NBconvert, you need to call `init_notebook_mode()` before using `show`).

You don't see any table above? Please either open the [HTML export](https://mwouts.github.io/itables/) of this notebook, or run this README on [Binder](https://mybinder.org/v2/gh/mwouts/itables/main?urlpath=lab/tree/README.md)!

## Supported environments

`itables` has been tested in the following editors:
- Jupyter Notebook
- Jupyter Lab
- Jupyter nbconvert (i.e. the tables are still interactive in the HTML export of a notebook)
- Google Colab
- VS Code (for both Jupyter Notebooks and Python scripts)
- PyCharm (for Jupyter Notebooks)
- Nteract

## Table not loading?

If the table just says "Loading...", then maybe
- You loaded a notebook that is not trusted (run "Trust Notebook" in View / Activate Command Palette)
- Or you are offline?

At the moment `itables` does not have an [offline mode](https://github.com/mwouts/itables/issues/8). While the table data is embedded in the notebook, the `jquery` and `datatables.net` are loaded from a CDN, see our [require.config](https://github.com/mwouts/itables/blob/main/itables/javascript/load_datatables_connected.js) and our [table template](https://github.com/mwouts/itables/blob/main/itables/datatables_template.html), so an internet connection is required to display the tables.

# Advanced usage

As `itables` is mostly a wrapper for the Javascript [datatables.net](https://datatables.net/) library, you should be able to find help on the datatables.net [forum](https://datatables.net/forums/) and [examples](https://datatables.net/examples/index)  for most formatting issues.

Below we give a few examples of how the datatables.net examples can be translated to Python with `itables`.

## Row sorting

Select the order in which the row are sorted with the [datatables' `order`](https://datatables.net/reference/option/order) argument. By default, the rows are sorted according to the first column (`order = [[0, 'asc']]`).

If you want to deactivate the sorting, set `order = []`, either in the `show` method, or as a global option:

```python
import pandas as pd
import itables.options as opt

opt.order = []  # no sorting
pd.DataFrame({'a':[2,1]})
```


## Pagination

### How many rows per page

Select [how many entries](https://datatables.net/examples/advanced_init/length_menu.html) should appear at once in the table with either the `lengthMenu` argument of the `show` function, or with the global option `itables.options.lengthMenu`:

```python
import itables.options as opt

opt.lengthMenu = [2, 5, 10, 20, 50, 100, 200, 500]
df
```

### Show the table in full

Show the table in full with the [`paging` argument](https://datatables.net/reference/option/paging), either in the `show` method, or in the options:

```python
show(df.head(), paging=False)
```

### Scroll

If you prefer to replace the pagination with a [vertical scroll](https://datatables.net/examples/basic_init/scroll_y.html), use for instance

```python
show(df, scrollY="200px", scrollCollapse=True, paging=False)
```

## Table and cell style

Select how your table should look like with the `classes` argument of the `show` function, or by changing `itables.options.classes`. For the list of possible values, see [datatables' default style](https://datatables.net/manual/styling/classes) and [the style examples](https://datatables.net/examples/styling/).

```python
opt.classes = ["display", "nowrap"]
df
```

```python
opt.classes = ["display", "cell-border"]
df
```

## Float precision

Floats are rounded using `pd.options.display.float_format`. Please change that format according to your preference.

```python
import math
import pandas as pd

with pd.option_context("display.float_format", "{:,.2f}".format):
    show(pd.Series([i * math.pi for i in range(1, 6)]))
```

You may also choose to convert floating numbers to strings:

```python
with pd.option_context("display.float_format", "${:,.2f}".format):
    show(pd.Series([i * math.pi for i in range(1, 6)]))
```

## Advanced cell formatting with JS callbacks

You can use Javascript callbacks to set the cell or row style depending on the cell content.

The example below, in which we color in red the cells with negative numbers, is directly inspired by the corresponding datatables.net [example](https://datatables.net/reference/option/columns.createdCell).

```python
show(
    pd.DataFrame([[-1, 2, -3, 4, -5], [6, -7, 8, -9, 10]], columns=list("abcde")),
    columnDefs=[
        {
            "targets": "_all",
            "createdCell": """
function (td, cellData, rowData, row, col) {
    if (cellData < 0) {
        $(td).css('color', 'red')
    }
}
""",
        }
    ],
    eval_functions=True,
)
```

## Column width

For tables that are larger than the notebook, the `columnDefs` argument allows to specify the desired width. If you wish you can also change the default in `itables.options`.

```python
show(x.to_frame().T, columnDefs=[{"width": "120px", "targets": "_all"}], maxColumns=300)
```

## Cell alignment

You can use the datatables.net [cell classes](https://datatables.net/manual/styling/classes#Cell-classes) like `dt-left`, `dt-center`, `dt-right` etc to set the cell alignment. Specify it for one table by using the `columnDefs` argument of `show`

```python
show(df, columnDefs=[{"className":"dt-center",  "targets": "_all"}])
```

or globally by setting `opt.columnDefs`:

```python
opt.columnDefs = [{"className":"dt-center", "targets": "_all"}]
df
```

```python
del opt.columnDefs
```

## HTML in cells

```python
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

## Select rows

Not currently implemented. May be made available at a later stage using the [select](https://datatables.net/extensions/select/) extension for datatables.


## Copy, CSV, PDF and Excel buttons

Not currently implemented. May be made available at a later stage thanks to the [buttons](https://datatables.net/extensions/buttons/) extension for datatable.


## <a name="downsampling"></a> Downsampling

When the data in a table is larger than `maxBytes`, which is equal to 64KB by default, `itables` will display only a subset of the table - one that fits into `maxBytes`. If you wish, you can deactivate the limit with `maxBytes=0`, change the value of `maxBytes`, or similarly set a limit on the number of rows (`maxRows`, defaults to 0) or columns (`maxColumns`, defaults to `pd.get_option('display.max_columns')`).

Note that datatables support [server-side processing](https://datatables.net/examples/data_sources/server_side). At a later stage we may implement support for larger tables using this feature.

```python
df = wb.get_indicators().head(500)
opt.maxBytes = 10000
df.values.nbytes
```

```python
df
```

To show the table in full, we can modify the value of `maxBytes` either locally:

```python
show(df, maxBytes=0)
```

or globally:

```python
opt.maxBytes = 2**20
df
```

# References

## DataTables

- DataTables is a plug-in for the jQuery Javascript library. It has a great [documentation](https://datatables.net/manual/), and a large set of [examples](https://datatables.net/examples/index).
- The R package [DT](https://rstudio.github.io/DT/) uses [datatables.net](https://datatables.net/) as the underlying library for both R notebooks and Shiny applications. In addition to the standard functionalities of the library (display, sort, filtering and row selection), RStudio seems to have implemented cell edition.

## Alternatives

ITables uses basic Javascript. It is not a Jupyter widget, which means that it does not allows you to **edit** the content of the dataframe.

If you are looking for Jupyter widgets, have a look at
- [QGrid](https://github.com/quantopian/qgrid) by Quantopian
- [IPyaggrid](https://dgothrek.gitlab.io/ipyaggrid/) by Louis Raison and Olivier Borderies
- [IPySheet](https://github.com/QuantStack/ipysheet) by QuantStack.

If you are looking for a table component that will fit in Dash applications, see [datatable by Dash](https://github.com/plotly/dash-table/).

Please also checkout [D-Tale](https://github.com/man-group/dtale) for exploring your Python DataFrames in the browser, using a local server.

<script async defer src="https://buttons.github.io/buttons.js"></script>
