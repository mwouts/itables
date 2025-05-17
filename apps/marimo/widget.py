import marimo

__generated_with = "0.13.6"
app = marimo.App()


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    # Using the ITable Widget in Marimo

    The `ITable` widget depends on [AnyWidget](https://anywidget.dev) -
    a great widget development framework! You can install it with
    ```bash
    pip install itables[widget]
    ```

    The `ITable` class accepts the same [options](../options/options.md) as the `show` method, but
    the `df` argument is optional.
    """
    )
    return


@app.cell
def _():
    from itables.sample_dfs import get_dict_of_test_dfs
    from itables.widget import ITable

    df = get_dict_of_test_dfs()["int_float_str"]

    table = ITable(df, selected_rows=[0, 2, 5], select=True)
    table  # type: ignore[reportUnusedExpression]
    return df, table


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    💡 The table shown above does not reflect the initial row selection.
    This is because the `ITable` widget was updated with
    more row selection commands, see below.

    ## The `selected_rows` traits

    ⚠️ At the moment, the selected rows are not displayed properly in Marimo.
    Please subscribe to https://github.com/mwouts/itables/issues/383 or reach out if you know how to fix this.

    The `selected_rows` attribute of the `ITable` object provides a view on the
    rows that have been selected in the table (remember to pass [`select=True`](../options/select.md) to activate the row selection). You can use it to either retrieve
    or change the current row selection:
    """
    )
    return


@app.cell
def _(table):
    table.selected_rows
    return


@app.cell
def _(table):
    table.selected_rows = [3, 4]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## The `df` property

    Use it to retrieve the table data:
    """
    )
    return


@app.cell
def _(table):
    table.df.iloc[table.selected_rows]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""or to update it""")
    return


@app.cell
def _(df, table):
    table.df = df.head(6)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    💡 `ITable` raises an `IndexError` if the `selected_rows` are not consistent with the data. If you need to update both simultaneously, use `table.update(df, selected_rows=...)`, see below.

    ## The `caption`, `style` and `classes` traits

    You can update these traits from Python, e.g.
    """
    )
    return


@app.cell
def _(table):
    table.caption = "numbers and strings"
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## The `update` method

    Last but not least, you can update the `ITable` arguments simultaneously using the `update` method:
    """
    )
    return


@app.cell
def _(df, table):
    table.update(df.head(20), selected_rows=[7, 8])
    return


@app.cell
def _():
    import marimo as mo

    return (mo,)


if __name__ == "__main__":
    app.run()
