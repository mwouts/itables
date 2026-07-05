from typing import Optional

from dash import callback  # pyright: ignore[reportUnknownVariableType]
from dash import Dash, Input, Output, html
from itables_core.sample_dfs import get_countries
from pyaggrid.dash import AgGrid

app = Dash(__name__)

df = get_countries()

app.layout = html.Div(
    [
        html.H1("PyAgGrid in a Dash application"),
        AgGrid(
            id="my_dataframe",
            df=df,
            caption="A DataFrame displayed with PyAgGrid",
            rowSelection={"mode": "multiRow"},
        ),
        html.Div(id="output"),
    ]
)


@callback(
    Output("output", "children"),
    Input("my_dataframe", "selected_rows"),
)
def show_selection(selected_rows: Optional["list[int]"]) -> str:
    return f"Selected rows: {selected_rows}"


if __name__ == "__main__":
    app.run(debug=True)  # pyright: ignore[reportUnknownMemberType]
