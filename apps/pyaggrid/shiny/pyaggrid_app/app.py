from itables_core.sample_dfs import get_dict_of_test_dfs
from pyaggrid import to_html_aggrid
from shiny.express import input, render, ui

dfs = get_dict_of_test_dfs()

ui.page_opts(title="Using pyaggrid in a Shiny App", fillable=True)

with ui.card():
    with ui.layout_sidebar():
        with ui.sidebar():
            ui.input_select(
                "table_selector",
                "Table",
                choices=list(dfs.keys()),
                selected="int_float_str",
            )
            ui.input_select(
                "theme",
                "Theme",
                choices=["quartz", "balham", "material", "alpine"],
            )

        @render.ui
        def my_table():
            """
            This function renders the table with pyaggrid. The HTML
            representation of the table loads AG Grid from the internet.
            """
            df = dfs[input.table_selector()]
            return ui.HTML(to_html_aggrid(df, theme=input.theme()))
