from pydatatables.sample_dfs import get_dict_of_test_dfs
from pydatatables.shiny import DataTable, init_pydatatables
from shiny.express import input, render, ui

dfs = get_dict_of_test_dfs()

ui.page_opts(title="Using DataTable in a Shiny App", fillable=True)

with ui.card():
    with ui.layout_sidebar():
        with ui.sidebar():
            ui.input_select(
                "table_selector",
                "Table",
                choices=list(dfs.keys()),
                selected="int_float_str",
            )

        ui.HTML(init_pydatatables())

        @render.ui
        def my_table():
            """
            This function renders the table using "DataTable".
            """
            df = dfs[input.table_selector()]
            return ui.HTML(DataTable(df, caption="A table rendered with ITable"))
