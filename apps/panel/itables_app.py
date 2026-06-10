"""
Run this app with:

pixi run -e panel-app panel serve apps/panel/itables_app.py
"""

import panel as pn

from itables.sample_dfs import get_dict_of_test_dfs
from itables.widget import ITable

# The "ipywidgets" extension (which requires the ipywidgets_bokeh
# and ipykernel packages) lets Panel render ipywidgets like the ITable widget
pn.extension("ipywidgets")

dfs = get_dict_of_test_dfs()
names = list(dfs.keys())

initial = names.index("int_float_str")

# ── Main table with row selection ──────────────────────────────────────────────

table = ITable(caption="A table rendered with ITable", select=True)

table_tabs = pn.Tabs(
    *[(name, pn.pane.Str("")) for name in names],
    active=initial,
    dynamic=True,
)

selected_rows = pn.pane.Markdown()


def on_tab_change(event) -> None:
    df = dfs[names[event.new]]
    table.update(df, selected_rows=list(range(0, len(df), 3)))


def on_selected_rows_change(change) -> None:
    selected_rows.object = f"Selected rows: `{change['new']}`"


table.observe(on_selected_rows_change, names="selected_rows")
table_tabs.param.watch(on_tab_change, "active")
on_tab_change(type("e", (), {"new": initial})())

# ── App layout ─────────────────────────────────────────────────────────────────

pn.template.FastListTemplate(
    title="Using the ITable Widget in a Panel App",
    logo="https://raw.githubusercontent.com/mwouts/itables/main/src/itables/logo/logo.svg",
    main=[
        table_tabs,
        pn.panel(table, sizing_mode="stretch_width"),
        selected_rows,
    ],
).servable()
