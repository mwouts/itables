# Dash

PyAgGrid does not have a native Dash component yet, so we embed the HTML
representation returned by `to_html_aggrid` in an `Iframe`, like in this
example:

```{include} ../../../apps/pyaggrid/dash/app.py
:code: python
```

```{tip}
For a native AG Grid component in Dash, with callbacks on the grid state,
see the official [dash-ag-grid](https://dash.plotly.com/dash-ag-grid)
package. And if you need callbacks with the look of DataTables, see the
`DataTable` component of [`pydatatables`](../../pydatatables/apps/dash.html).
```
