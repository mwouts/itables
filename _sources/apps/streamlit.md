# Streamlit

To display Python DataFrames as interactive DataTables in Streamlit applications, use

```
from itables.streamlit import interactive_table
```

We have a sample application available at https://itables.streamlit.app (source code [here](https://github.com/mwouts/demo_itables_in_streamlit/blob/main/itables_app.py))

```{div} full-width
<iframe src="https://itables.streamlit.app?embed=true"
style="height: 600px; width: 100%;"></iframe>
```

## Selected rows

Use the `selected_rows: list[int]` argument from `interactive_table` to
select rows when the table is first displayed. Add `select=True` to let the user modify the selection. Then, the `interactive_table` component returns a dict, with a key `"selected_rows"` that points to the updated selection.

## Using HTML

Before ITables v2.4.0, the streamlit component was missing a few options compared to the HTML implementation. A possible fallback was to use `to_html_datatable` in combination with Streamlit's `html` function - but you should not need that anymore with the latest version of ITables.

Please note that:
- you will have to specify the table height manually,
- an internet connection is required when using `to_html_datatable`,
- the app/table might take longer to display.

A sample application is available at https://to-html-datatable.streamlit.app (source code [here](https://github.com/mwouts/to_html_datatable_in_streamlit/blob/main/itables_app.py))

```{div} full-width
<iframe src="https://to-html-datatable.streamlit.app?embed=true"
style="height: 600px; width: 100%;"></iframe>
```
