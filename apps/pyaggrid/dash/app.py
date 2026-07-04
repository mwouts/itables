"""Display a DataFrame with pyaggrid in a Dash application.

pyaggrid does not have a native Dash component yet, so we embed its
HTML representation in an Iframe. For a native AG Grid component in
Dash, see also the official dash-ag-grid package.
"""

from dash import Dash, html
from itables_core.sample_dfs import get_countries
from pyaggrid import to_html_aggrid

app = Dash(__name__)

df = get_countries()

app.layout = html.Div(
    [
        html.H1("PyAgGrid in a Dash application"),
        html.Iframe(
            srcDoc=to_html_aggrid(df, caption="A DataFrame displayed with pyaggrid"),
            style={"width": "100%", "height": "700px", "border": "none"},
        ),
    ]
)

if __name__ == "__main__":
    app.run(debug=True)  # pyright: ignore[reportUnknownMemberType]
