# Run this app with "shiny run file.py"
from shiny import App, ui

from itables.sample_dfs import get_dict_of_test_dfs
from itables.shiny import DT

app_ui = ui.page_fluid(
    # Display the different tables in different tabs
    ui.navset_tab(
        *[
            ui.nav_panel(name, ui.HTML(DT(df)))
            for name, df in get_dict_of_test_dfs().items()
        ]
    )
)

app = App(app_ui, server=None)
