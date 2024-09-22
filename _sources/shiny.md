# Shiny

You can use ITables in Web applications generated with [Shiny](https://shiny.rstudio.com/py/) for Python with e.g.
```python
from shiny import ui

from itables.sample_dfs import get_countries
from itables.shiny import DT, init_itables

# Load the datatables library and css from the ITables package
# (use connected=True if you prefer to load it from the internet)
ui.HTML(init_itables(connected=False))

# Render the table with DT
ui.HTML(DT(get_countries(html=False)))
```

If you enable row selection and set an id on your table, e.g. `DT(df, table_id="my_table", select=True)` then
ITables will provide the list of selected rows at `input.my_table_selected_rows()` (replace `my_table` with your
own table id).

See also our [tested examples](https://github.com/mwouts/itables/tree/main/tests/sample_python_apps).
