# Pandas DataFrames and Series as Interactive Tables in Jupyter

[![Build Status](https://travis-ci.com/mwouts/itables.svg?branch=master)](https://travis-ci.com/mwouts/itables)
[![codecov.io](https://codecov.io/github/mwouts/itables/coverage.svg?branch=master)](https://codecov.io/github/mwouts/itables?branch=master)

Turn pandas DataFrames and Series into interactive [datatables](https://datatables.net) in both your notebooks and their HTML representation with a single additional import:

```python
import itables.interactive
import world_bank_data as wb
df = wb.get_countries()
df
```

![](https://gist.githubusercontent.com/mwouts/165badb3f8ab345a25739a792859583b/raw/43d66231a1f916b350d266a8cb503dd30d7ae1e2/datatables.png)

# Quick start

Install the package with

```
pip install itables
```

Activate the interactive mode for all series and dataframes with 

```python
import itables.interactive
```

Display just one series or dataframe as an interactive table with the `show` function.

```python
from itables import show
x = wb.get_series('SP.POP.TOTL', mrv=1, simplify_index=True)
show(x)
```

# Advanced usage

## Pagination

### How many rows per page

Select [how many entries](https://datatables.net/examples/advanced_init/length_menu.html) should appear at once in the table with the `lengthMenu` argument of the `show` function, or by changing `itables.options.default`:

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
opt.classes = ['display', 'nowrap']
df
```

```python
opt.classes = ['display', 'cell-border']
df
```

## Float precision

Floats are rounded using `pd.options.display.float_format`. Please change that format according to your preference.

```python
import math
import pandas as pd
with pd.option_context('display.float_format', '{:,.2f}'.format):
    show(pd.Series([i * math.pi for i in range(1,6)]))
```

You may also choose to convert floating numbers to strings:

```python
with pd.option_context('display.float_format', '${:,.2f}'.format):
    show(pd.Series([i * math.pi for i in range(1,6)]))
```

## Advanced cell formatting

Datatables allows to set the cell or row style depending on the cell content, with either the [createdRow](https://datatables.net/reference/option/createdRow) or [createdCell](https://datatables.net/reference/option/columns.createdCell) callback. For instance, if we want the cells with negative numbers to be colored in red, we can use the `columnDefs.createdCell` argument as follows:

```python
show(pd.DataFrame([[-1,2,-3,4,-5],[6,-7,8,-9,10]], columns=list('abcde')), 
                 columnDefs = [ { "targets": "_all",
    "createdCell": """function (td, cellData, rowData, row, col) {
      if ( cellData < 0 ) {
        $(td).css('color', 'red')
      }
    }"""
  } ])
```

## Column width

FIXME: This does not appear to be working...

```python
show(df, columnsDefs = [{ "width": "200px", 'target':3}])
```

But in some cases - a table with many column like the one below, we can use the `width` parameter...

```python
show(x.to_frame().T, columnDefs = [{ "width": "80px", "targets": "_all" }])
```

## HTML in cells

```python
import pandas as pd
show(pd.Series(['<b>bold</b>', '<i>italic</i>', '<a href="https://github.com/mwouts/itables">link</a>'], name='HTML'), paging=False)
```

## Select rows

Not currently implemented. May be made available at a later stage using the [select](https://datatables.net/extensions/select/) extension for datatables.


## Copy, CSV, PDF and Excel buttons

Not currently implemented. May be made available at a later stage thanks to the [buttons](https://datatables.net/extensions/buttons/) extension for datatable.


## Large table support

`itables` will not display dataframes that are larger than `maxBytes`, which is equal to 1MB by default. Truncate the dataframe with `df.head()`, or set the `maxBytes` parameter or option to an other value to display the dataframe. Or deactivate the limit with `maxBytes=0`.

Note that datatables support [server-side processing](https://datatables.net/examples/data_sources/server_side). At a later stage we may implement support for larger tables using this feature.

```python
df = wb.get_indicators()
df.values.nbytes
```

```python
opt.maxBytes = 1000000
df
```

# References

## DataTables

- DataTables is a plug-in for the jQuery Javascript library. It has a great [documentation](https://datatables.net/manual/), and a large set of [examples](https://datatables.net/examples/index).
- The R package [DT](https://rstudio.github.io/DT/) uses [datatables.net](https://datatables.net/) as the underlying library for both R notebooks and Shiny applications. In addition to the standard functionalities of the library (display, sort, filtering and row selection), RStudio seems to have implemented cell edition.
- Marek Cermak has an interesting [tutorial](https://medium.com/@marekermk/guide-to-interactive-pandas-dataframe-representation-485acae02946) on how to use datatables within Jupyter. He also published [jupyter-datatables](https://github.com/CermakM/jupyter-datatables), with a focus on numerical data and distribution plots.

## Alternatives

ITables is not a Jupyter widget, which means that it does not allows you to **edit** the content of the dataframe. 
If you are looking for Jupyter widgets, have a look at
- [QGrid](https://github.com/quantopian/qgrid) by Quantopian
- [IPyaggrid](https://dgothrek.gitlab.io/ipyaggrid/) by Louis Raison and Olivier Borderies
- [IPySheet](https://github.com/QuantStack/ipysheet) by QuantStack.

If you are looking for a table component that will fit in Dash applications, see [datatable by Dash](https://github.com/plotly/dash-table/).

## Contributing

I think it would be very helpful to have an identical table component for both Jupyter and [Dash](http://dash.plot.ly/). Please [let us know](https://community.plot.ly/t/why-does-dash-have-its-own-datatable-library/) if you are interested in drafting a new table component based on an existing Javascript library for Dash.

Also, if you happen to prefer another Javascript table library (say, [ag-grid](https://www.ag-grid.com/)), and you would like to see it supported in `itables`, please open either an issue or a PR, and let us know what is the minimal code to display a table in Jupyter using your library.
