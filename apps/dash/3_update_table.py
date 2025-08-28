"""
This is an example Dash application in which we update the table.

Launch the app by running `python 3_update_table.py`.
"""

import logging
from typing import Any, Optional

from dash import callback  # pyright: ignore[reportUnknownVariableType]
from dash import Dash, Input, Output, State, callback_context, dcc, html

from itables import DTForITablesOptions, ITableOptions
from itables.dash import (
    ITable,
    ITableOutputs,
    updated_itable_outputs,
)
from itables.sample_dfs import get_countries

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

app = Dash(__name__)

df = get_countries()

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
                            ["Select", "Buttons", "HTML", "ColumnControl"],
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
def update_table(
    checklist: Optional[list[str]],
    caption: Optional[str],
    selected_rows: Optional[list[int]],
    dt_args: Optional[DTForITablesOptions],
) -> list[Any]:
    if checklist is None:
        checklist = []

    kwargs: ITableOptions = {}

    # When df=None and when the dt_args don't change, the table is not updated
    df = None
    if callback_context.triggered_id in {  # pyright: ignore[reportUnknownMemberType]
        None,
        "checklist",
    }:
        df = get_countries(html="HTML" in checklist)

    kwargs["select"] = "Select" in checklist
    if "Buttons" in checklist:
        kwargs["buttons"] = ["copyHtml5", "csvHtml5", "excelHtml5"]

    if "HTML" in checklist:
        kwargs["allow_html"] = True

    if "ColumnControl" in checklist:
        kwargs["columnControl"] = ["order", "colVisDropdown", "searchDropdown"]
        kwargs["ordering"] = {"indicators": False, "handler": False}

    if selected_rows is not None:
        kwargs["selected_rows"] = selected_rows

    return updated_itable_outputs(
        df, caption=caption, current_dt_args=dt_args, **kwargs
    )


@callback(
    Output("output", "children"),
    Input("my_dataframe", "selected_rows"),
)
def show_selection(selected_rows: list[int]):
    return f"Selected rows: {selected_rows}"


if __name__ == "__main__":
    app.run(debug=True)  # pyright: ignore[reportUnknownMemberType]
