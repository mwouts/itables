# Shiny

## Using `ITable` in Shiny

The recommended way to use `ITables` in a [Shiny for Python](https://shiny.rstudio.com/py/) application is with the [ITable Widget](widget.md).

In the Shiny Express syntax this is as simple as:
```python
from shinywidgets import render_widget

from itables.widget import ITable


@render_widget
def my_table():
    """
    This function creates the "my_table" widget.
    """
    # Note: df is an optional argument
    return ITable(caption="A table rendered with ITable")
```

In the Shiny Core syntax you will need, in addition to the above,
to insert the table in the UI with `output_widget`:

```python
from shiny import ui
from shinywidgets import output_widget

app_ui = ui.page_fluid(
    # ...
    output_widget("my_table"),
    # ...
)
```

## Updating the widget

Rather than re-creating the widget each time the data changes, you can
call the `.update` method of the widget object, using the `@reactive.effect`
decorator:

```python
from shiny import reactive
from shiny.express import input

from itables.sample_dfs import get_dict_of_test_dfs

dfs = get_dict_of_test_dfs()


@reactive.effect
def _():
    """
    This "reactive.effect" calls the "update" method of the ITable widget
    to update the widget with the new inputs.
    """
    # Get the new inputs
    df = dfs[input.table_selector()]
    selected_rows = list(range(0, len(df), 3))

    # Update the widget
    my_table.widget.update(df, selected_rows=selected_rows)
```

## Accessing the `selected_rows` attribute

The `reactive_read` function lets you access the `selected_rows` attribute
of the `ITable` object. The code below displays the selected rows:

```python
from shiny.express import render
from shinywidgets import reactive_read


@render.code
def selected_rows():
    """
    Here we read the "selected_rows" attribute of the ITable widget
    """
    return str(reactive_read(my_table.widget, "selected_rows"))
```

## An example application

This [repository](https://github.com/mwouts/demo_itables_in_shiny-py/) contains a simple
example of a Shiny application that uses the `ITable` widget.

The source code of the application
is at [`app.py`](https://github.com/mwouts/demo_itables_in_shiny-py/blob/main/itable_widget/app.py)
(Shiny Express) or [`app-core.py`](https://github.com/mwouts/demo_itables_in_shiny-py/blob/main/itable_widget/app-core.py)
(Shiny Core).

```{div}
<iframe src="https://itables.shinyapps.io/itable_widget?embed=true"
style="height: 800px; width: 100%;"></iframe>
```

## Limitations

Compared to `show`, the `ITable` widget has the same limitations as the [Streamlit component](streamlit.md#limitations),
e.g. structured headers are not available, you can't pass JavaScript callback, etc.

The good news is that if you only want to _display_ the table, you do not need
the `ITable` widget. You can render the table using `HTML(DT(...))` as here:

```python
from shiny import ui

from itables.sample_dfs import get_countries
from itables.shiny import DT, init_itables

# Load the datatables library and css from the ITables package
# (use connected=True if you prefer to load it from the internet)
ui.HTML(init_itables())

# Render the table with DT
ui.HTML(DT(get_countries(html=False)))
```

An example for an application that uses `DT` is available at [`app.py`](https://github.com/mwouts/demo_itables_in_shiny-py/blob/main/itables_DT/app.py)
(Shiny Express) or [`app-core.py`](https://github.com/mwouts/demo_itables_in_shiny-py/blob/main/itables_DT/app-core.py)
(Shiny Core).

```{div}
<iframe src="https://itables.shinyapps.io/itables_DT?embed=true"
style="height: 800px; width: 100%;"></iframe>
```
