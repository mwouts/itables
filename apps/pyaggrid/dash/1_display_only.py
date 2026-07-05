from dash import Dash, html
from itables_core.sample_dfs import get_countries
from pyaggrid.dash import AgGrid

app = Dash(__name__)

df = get_countries()

app.layout = html.Div(
    [
        html.H1("PyAgGrid in a Dash application"),
        AgGrid(id="my_dataframe", df=df, caption="A DataFrame displayed with PyAgGrid"),
    ]
)

if __name__ == "__main__":
    app.run(debug=True)  # pyright: ignore[reportUnknownMemberType]
