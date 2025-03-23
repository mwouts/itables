from dash import Dash, Input, Output, callback, html

from itables.dash import ITable
from itables.sample_dfs import get_countries

app = Dash(__name__)

df = get_countries(html=False)

app.layout = html.Div(
    [
        html.H1("ITables in a Dash application"),
        ITable(
            id="my_dataframe",
            df=df,
            caption="A DataFrame displayed with ITables",
            select=True,
        ),
        html.Div(id="output"),
    ]
)


@callback(
    Output("output", "children"),
    Input("my_dataframe", "selected_rows"),
)
def show_selection(selected_rows):
    return f"Selected rows: {selected_rows}"


if __name__ == "__main__":
    app.run(debug=True)
