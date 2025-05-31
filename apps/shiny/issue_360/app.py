from shiny import App, ui
from shinywidgets import output_widget, render_widget

from itables.sample_dfs import get_countries
from itables.widget import ITable

app_ui = ui.page_fluid(
    ui.h1("Issue #360"),
    ui.p("The table height is not correct"),
    output_widget("my_table"),
    ui.p("More content, should not hide the table (but it does)"),
)


# Define server
def server(input, output, session):
    @render_widget
    def my_table():
        return ITable(df=get_countries(html=False))


# Create the Shiny app
app = App(app_ui, server)
