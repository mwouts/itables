import marimo

__generated_with = "0.13.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import pandas as pd

    from itables.widget import ITable

    df = pd.DataFrame({"x": [2, 1, 3], "y": list("cbc")})

    ITable(df, buttons=["pageLength", "copyHtml5", "csvHtml5", "excelHtml5", "colvis"])
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
