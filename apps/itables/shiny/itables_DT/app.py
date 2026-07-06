from itables.sample_dfs import get_dict_of_test_dfs
from itables.shiny import DT, init_itables
from shiny.express import input, render, ui

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

        ui.HTML(init_itables())

        @render.ui
        def my_table():
            """
            This function renders the table using "DT".
            """
            df = dfs[input.table_selector()]
            return ui.HTML(DT(df, caption="A table rendered with ITable"))
