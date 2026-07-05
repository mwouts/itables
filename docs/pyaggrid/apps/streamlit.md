# Streamlit

The `aggrid` [Streamlit](https://streamlit.io) component renders your
DataFrames with AG Grid in Streamlit applications. Install it with

```shell
pip install pyaggrid[streamlit]
```

then use it like here:

```{include} ../../../apps/pyaggrid/streamlit/app.py
:code: python
```

## Selected rows

Use the `selected_rows: list[int]` argument of `aggrid` to select rows when
the table is first displayed. Add `rowSelection={"mode": "multiRow"}` to let
the user modify the selection. The `aggrid` component returns a dict with a
key `"selected_rows"` that points to the updated selection.

```{tip}
See also the [streamlit-aggrid](https://github.com/PablocFonseca/streamlit-aggrid)
package, and the `datatable` component of
[`pydatatables`](../../pydatatables/apps/streamlit.html) for the DataTables look.
```
