from shiny import App, ui

from itables import to_html_datatable as DT
from itables.sample_dfs import get_countries

df = get_countries()

app_ui = ui.page_fluid(ui.HTML(DT(df)))

app = App(app_ui, server=None)
# app.run()
