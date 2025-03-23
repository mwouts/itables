from dash import Dash, html

from itables.dash import ITable
from itables.sample_dfs import get_countries

app = Dash(__name__)

df = get_countries(html=False)

app.layout = html.Div(
    [
        html.H1("ITables in a Dash application"),
        ITable(id="my_dataframe", df=df, caption="A DataFrame displayed with ITables"),
    ]
)

if __name__ == "__main__":
    app.run(debug=True)
