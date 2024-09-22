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

This feature was added in ITables v2.2.0.

Use the `selected_rows: list[int]` argument from `interactive_table` to
select rows when the table is first displayed. Add `select=True` to let the user modify the selection. Then, the `interactive_table` component returns a dict, with a key `"selected_rows"` that points to the updated selection.

## Limitations

In most cases, you will be able to use `interactive_table` in a
Streamlit application in the same way that you use `show` in notebooks.

Due to implementation constraints, the Streamlit component has some limitations
that `show` does not have:
- Pandas Style objects can't be rendered with `interactive_table`. This is because
the Streamlit component needs to pass the table data to the frontend in JSON format (while Pandas Style objects are formatted using HTML)
- Similarly, you can't use the `use_to_html` argument in `interactive_table`
- Complex column headers might look different than in notebooks, and HTML in columns is not supported
- JavaScript callbacks like custom formatting functions are not supported
- The interactive table is rendered within an iframe that has a fixed weight. This does not work well with the `lengthMenu` control, nor with the advanced filtering extensions (if that is an issue for you, please subscribe or contribute to [#275](https://github.com/mwouts/itables/issues/275)).

## Workaround

If you hit one of the limitations above, you can fallback to using `to_html_datatable` in combination with Streamlit's `html` function.

Please note that:
- you will have to specify the table height manually,
- an internet connection is required when using `to_html_datatable`,
- the app/table might take longer to display.

A sample application is available at https://to-html-datatable.streamlit.app (source code [here](https://github.com/mwouts/to_html_datatable_in_streamlit/blob/main/itables_app.py))

```{div} full-width
<iframe src="https://to-html-datatable.streamlit.app?embed=true"
style="height: 600px; width: 100%;"></iframe>
```
