# Run this app with "shiny run file.py"
from shiny import App, Inputs, Outputs, Session, render, ui

from itables.sample_dfs import get_countries
from itables.shiny import DT, init_shiny_mode

app_ui = ui.page_fluid(
    ui.HTML(init_shiny_mode()),
    ui.layout_columns(
        ui.value_box(
            "Selected rows",
            ui.output_ui("selected_rows"),
        ),
        fill=False,
    ),
    ui.layout_columns(
        ui.card(ui.output_ui("table"), full_screen=True),
    ),
    title="ITables in a Shiny App",
)


def server(input: Inputs, output: Outputs, session: Session):
    @render.ui
    def table():
        return ui.HTML(
            DT(
                get_countries(html=False),
                table_id="countries",
                select=True,
                selected_rows=[0, 1, 2, 207],
            )
        )

    @render.ui
    def selected_rows():
        selected_rows = list(input.countries_selected_rows())
        return f"You have selected {len(selected_rows)} rows: {selected_rows}"


app = App(app_ui, server, debug=True)
