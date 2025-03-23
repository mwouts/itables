"""
This is an example Dash application that uses the ITable component.

Launch the app by running `python app.py`.
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


app.layout = html.Div(
    [
        html.H1("DataTable in a Dash application"),
        dcc.Checklist(
            ["Select", "Buttons", "HTML"],
            ["Select"],
            id="checklist",
        ),
        dcc.Input(id="caption", value="table caption"),
        ITable(id="my_dataframe", df=df),
        html.Div(id="output"),
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
    if callback_context.triggered_id == "checklist":
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
