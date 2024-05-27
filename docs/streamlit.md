# Streamlit

ITables in version `2.1.0` or above can be used in Streamlit.

To render a DataFrame with ITables in a Streamlit app, use `interactive_table`:
```
from itables.streamlit import interactive_table
```

The function `interactive_table` accepts the same arguments as `show` and `to_html_datatable`, e.g. the
first argument is the dataframe that will be displayed, and then you
can set a `caption`, custom `classes` or `style`, and even activate the `buttons` extension, etc...

Unlike `show`, `interactive_table` has `scrollX=True` by default. This makes the
rendering of wide tables more similar to that of `show` in Notebooks.

## A sample application

A sample Streamlit application is available at [itables.streamlit.app](https://itables.streamlit.app) (source code [here](https://github.com/mwouts/demo_itables_in_streamlit/blob/main/itables_app.py))

<iframe src="https://itables.streamlit.app?embed=true"
style="height: 600px; width: 100%;"></iframe>

## Limitations of ITables in Streamlit

From a user perspective, you will be able to use `interactive_table` in a
Streamlit application in the same way that you use `show` in notebooks.

Due to implementation constraints, the Streamlit component has some limitations
that `show` does not have:
- Pandas Style objects can't be rendered with `interactive_table`. This is because
the Streamlit component needs to pass the table data to the frontend in JSON format (while Pandas Style objects are formatted using HTML)
- Similarly, you can't use the `use_to_html` argument in `interactive_table`
- Complex column headers might look different than in notebooks, and HTML in columns is not supported
- JavaScript callbacks like custom formatting functions are not supported
- The interactive table is rendered within an iframe that has a fixed weight. This does not work well with the `lengthMenu` control, nor with the advanced filtering extensions (if that is an issue for you, please subscribe or contribute to [#275](https://github.com/mwouts/itables/issues/275)).

## Future developments

ITables' Streamlit component might see the following developments in the future
- Return the selected cells
- Make the table editable (will require a DataTable [editor license](https://editor.datatables.net/purchase/))
