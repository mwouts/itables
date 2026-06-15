from shiny import App, render, ui

from pydatatables.sample_dfs import get_dict_of_test_dfs
from pydatatables.shiny import DataTable, init_pydatatables

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
    ui.HTML(init_pydatatables()),
    ui.output_ui("my_table"),
    ui.markdown("Selected rows"),
    ui.output_code("selected_rows"),
    title="Using DataTable in a Shiny App",
    fillable=True,
)


def server(input, output, session):  # type: ignore
    @render.ui
    def my_table():  # pyright: ignore[reportUnusedFunction]
        """
        This function renders the table using "DataTable".
        """
        df = dfs[input.table_selector()]  # pyright: ignore[reportUnknownMemberType]

        return ui.HTML(DataTable(df))


app = App(app_ui, server)  # pyright: ignore[reportUnknownArgumentType]
