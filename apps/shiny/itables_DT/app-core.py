from shiny import App, render, ui

from itables.sample_dfs import get_dict_of_test_dfs
from itables.shiny import DT, init_itables

dfs = get_dict_of_test_dfs()

app_ui = ui.page_sidebar(
    ui.sidebar(
        ui.input_select(
            "table_selector",
            "Table",
            choices=list(dfs.keys()),
            selected="int_float_str",
        )
    ),
    ui.HTML(init_itables()),
    ui.output_ui("my_table"),
    ui.markdown("Selected rows"),
    ui.output_code("selected_rows"),
    title="Using DT in a Shiny App",
    fillable=True,
)


def server(input, output, session):
    @render.ui
    def my_table():
        """
        This function renders the table using "DT".
        """
        df = dfs[input.table_selector()]

        return ui.HTML(DT(df))


app = App(app_ui, server)
