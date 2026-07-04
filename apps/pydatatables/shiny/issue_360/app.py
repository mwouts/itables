from pydatatables.sample_dfs import get_countries
from pydatatables.widget import DataTable
from shiny import App, ui
from shinywidgets import output_widget, render_widget

app_ui = ui.page_fluid(
    ui.h1("Issue #360"),
    ui.p("The table height is not correct"),
    output_widget("my_table", fillable=False),
    ui.p(
        "More content, should not hide the table (but it does when "
        "we don't set `fillable=False` in `output_widget`)"
    ),
)


# Define server
def server(
    input,  # pyright: ignore[reportUnknownParameterType,reportMissingParameterType]
    output,  # pyright: ignore[reportUnknownParameterType,reportMissingParameterType]
    session,  # pyright: ignore[reportUnknownParameterType,reportMissingParameterType]
):
    @render_widget
    def my_table():  # pyright: ignore[reportUnusedFunction]
        return DataTable(df=get_countries())


# Create the Shiny app
app = App(app_ui, server)  # pyright: ignore[reportUnknownArgumentType]
