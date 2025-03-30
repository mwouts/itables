"""
This is an example Dash application in which we update the table.

Launch the app by running `python 3_update_table.py`.
"""

import logging

from dash import Dash, Input, Output, State, callback, callback_context, dcc, html

from itables.dash import ITable, ITableOutputs, updated_itable_outputs
from itables.sample_dfs import get_countries

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

app = Dash(__name__)

df = get_countries(html=False)

# Create the layout with sidebar
app.layout = html.Div(
    [
        html.Div(
            className="container",
            children=[
                # Sidebar
                html.Div(
                    className="sidebar",
                    children=[
                        html.H2("Controls"),
                        html.Label("Table Options:"),
                        dcc.Checklist(
                            ["Select", "Buttons", "HTML"],
                            ["Select"],
                            id="checklist",
                            style={"marginBottom": "20px"},
                        ),
                        html.Label("Table Caption:"),
                        dcc.Input(
                            id="caption",
                            value="table caption",
                            style={"width": "100%", "marginBottom": "20px"},
                        ),
                    ],
                ),
                # Main content
                html.Div(
                    className="main-content",
                    children=[
                        html.H1("ITable in a Dash application"),
                        ITable(id="my_dataframe"),
                        html.Div(id="output", style={"marginTop": "20px"}),
                    ],
                ),
            ],
        )
    ]
)


@callback(
    ITableOutputs("my_dataframe"),
    [
        Input("checklist", "value"),
        Input("caption", "value"),
        State("my_dataframe", "selected_rows"),
        State("my_dataframe", "dt_args"),
    ],
)
def update_table(checklist, caption, selected_rows, dt_args):
    if checklist is None:
        checklist = []

    kwargs = {}

    # When df=None and when the dt_args don't change, the table is not updated
    if callback_context.triggered_id in {None, "checklist"}:
        kwargs["df"] = get_countries(html="HTML" in checklist)

    kwargs["select"] = "Select" in checklist
    if "Buttons" in checklist:
        kwargs["buttons"] = ["copyHtml5", "csvHtml5", "excelHtml5"]

    return updated_itable_outputs(
        caption=caption, selected_rows=selected_rows, current_dt_args=dt_args, **kwargs
    )


@callback(
    Output("output", "children"),
    Input("my_dataframe", "selected_rows"),
)
def show_selection(selected_rows):
    return f"Selected rows: {selected_rows}"


if __name__ == "__main__":
    app.run(debug=True)
