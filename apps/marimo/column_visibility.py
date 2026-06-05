# /// script
# requires-python = ">=3.12,<3.13"
# dependencies = [
#     "anywidget==0.9.18",
#     "pydatatables==2.4.0",
#     "marimo",
#     "pandas==2.2.3",
# ]
# ///

import marimo

__generated_with = "0.13.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import pandas as pd

    from pydatatables.widget import PyDataTablesRenderer

    df = pd.DataFrame({"x": [2, 1, 3], "y": list("cbc")})

    # buttons that trigger a drop-down don't work in Marimo when using the widget
    # see below for a workaround using mo.iframe
    ITable(df, buttons=["pageLength", "copyHtml5", "csvHtml5", "excelHtml5", "colvis"])
    return (df,)


@app.cell
def _(df):
    import marimo as mo

    import pydatatables

    html = pydatatables.to_html_datatable(
        df,
        buttons=["pageLength", "copyHtml5", "csvHtml5", "excelHtml5", "colvis"],
        connected=True,
    )
    mo.iframe(html)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
