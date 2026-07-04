# Streamlit

PyAgGrid does not have a native Streamlit component yet, so we embed the
HTML representation returned by `to_html_aggrid` with
`st.components.v1.html`, like in this example:

```{include} ../../../apps/streamlit/pyaggrid_app.py
:code: python
```

Please note that:
- you have to specify the component height manually,
- an internet connection is required when the table is displayed.

```{tip}
See also the [streamlit-aggrid](https://github.com/PablocFonseca/streamlit-aggrid)
package for a native AG Grid component in Streamlit, and the
`datatable` component of [`pydatatables`](../../apps/streamlit.html)
for the DataTables look with selection callbacks.
```
