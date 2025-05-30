import marimo

__generated_with = "0.13.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import pandas as pd

    from itables.widget import ITable

    df = pd.DataFrame({"i": range(6)})

    w = ITable(df, select=True, selected_rows=[1, 4])
    w
    return (w,)


@app.cell
def _(w):
    w._css
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
