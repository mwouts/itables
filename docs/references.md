# References

## DataTables

- DataTables is a plug-in for the jQuery Javascript library. It has a great [documentation](https://datatables.net/manual/), and a large set of [examples](https://datatables.net/examples/index).
- The R package [DT](https://rstudio.github.io/DT/) uses [DataTables](https://datatables.net/) as the underlying library for both R notebooks and Shiny applications. In addition to the standard functionalities of the library (display, sort, filtering and row selection), RStudio seems to have implemented cell edition.

## Alternatives

ITables uses basic Javascript. It is not a Jupyter widget, which means that it does not allows you to **edit** the content of the dataframe.

If you are looking for Jupyter widgets, have a look at
- [QGrid](https://github.com/quantopian/qgrid) by Quantopian
- [IPyaggrid](https://dgothrek.gitlab.io/ipyaggrid/) by Louis Raison and Olivier Borderies
- [IPySheet](https://github.com/QuantStack/ipysheet) by QuantStack.

If you are looking for a table component that will fit in Dash applications, see [datatable by Dash](https://github.com/plotly/dash-table/).

Please also checkout [D-Tale](https://github.com/man-group/dtale) for exploring your Python DataFrames in the browser, using a local server.
