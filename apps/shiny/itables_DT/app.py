from shiny.express import input, render, ui

from pydatatables.sample_dfs import get_dict_of_test_dfs
from pydatatables.shiny import DT, init_pydatatables

dfs = get_dict_of_test_dfs()

ui.page_opts(title="Using DT in a Shiny App", fillable=True)

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
            This function renders the table using "DT".
            """
            df = dfs[input.table_selector()]
            return ui.HTML(DT(df, caption="A table rendered with ITable"))
