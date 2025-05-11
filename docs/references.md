# References

ITables is a wrapper for the [datatables-net](https://datatables.net) Javascript library, for Python. That library is developped by [SpryMedia](https://sprymedia.co.uk/) and made available under a MIT license. It has an extensive [documentation](https://datatables.net/manual/), as well as a large set of [examples](https://datatables.net/examples/index).

## ITables and its alternatives

### Jupyter Widgets

In Jupyter or VS Code, ITables can render your dataframes using either HTML (with either `init_notebook_mode()`, or `init_notebook_mode(all_interactive=False)` and `show`) or the [`ITable` widget](apps/widget.md).

Other Jupyter widgets that let you render a dataframe in Jupyter are
- [QGrid](https://github.com/quantopian/qgrid) by Quantopian
- [IPyaggrid](https://dgothrek.gitlab.io/ipyaggrid/) by Louis Raison and Olivier Borderies
- [IPySheet](https://github.com/QuantStack/ipysheet) by QuantStack.

### Dash component

Since ITables v2.3.0 you can use our [`ITable` component](apps/dash.md) in Dash applications.

Alternatives for rendering DataFrames in Dash are
- [Dash DataTable](https://dash.plotly.com/datatable)
- [Dash AG Grid](https://dash.plotly.com/dash-ag-grid).

### Streamlit

In ITables v2.1.0 we added the [`interactive_table` component](apps/streamlit.md) that can be used in Streamlit applications.

Alternative for rendering DataFrames in Streamlit are
- [`st.dataframe`](https://docs.streamlit.io/develop/api-reference/data/st.dataframe)
- [`streamlit-aggrid`](https://github.com/PablocFonseca/streamlit-aggrid).

### DT in R

The R package [DT](https://rstudio.github.io/DT/) is a wrapper for [DataTables](https://datatables.net/) that you can use both in R notebooks and R Shiny applications.

### D-Tale

[D-Tale](https://github.com/man-group/dtale) lets you explore your Python DataFrames in the browser, using a local server.
