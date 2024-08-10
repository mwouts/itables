# Run this app with "shiny run file.py"
from shiny import App, ui

from itables.sample_dfs import get_dict_of_test_dfs
from itables.shiny import DT

try:
    # This one is not available on the CI (Python 3.8)
    ui_nav = ui.nav
except AttributeError:
    ui_nav = ui.nav_panel

app_ui = ui.page_fluid(
    # Display the different tables in different tabs
    ui.navset_tab(
        *[ui_nav(name, ui.HTML(DT(df))) for name, df in get_dict_of_test_dfs().items()]
    )
)

app = App(app_ui, server=None)
