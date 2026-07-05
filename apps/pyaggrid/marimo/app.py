import marimo

__generated_with = "0.13.6"
app = marimo.App()


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Using the AgGrid Widget in Marimo

    The `AgGrid` widget depends on [AnyWidget](https://anywidget.dev). You can install it with
    ```bash
    pip install pyaggrid[widget]
    ```

    The `AgGrid` class accepts the same options as the `show` method, but
    the `df` argument is optional.
    """)
    return


@app.cell
def _():
    from itables_core.sample_dfs import get_dict_of_test_dfs
    from pyaggrid.widget import AgGrid

    df = get_dict_of_test_dfs()["int_float_str"]

    table = AgGrid(df, selected_rows=[0, 2, 5], rowSelection={"mode": "multiRow"})
    table  # type: ignore[reportUnusedExpression]
    return (table,)


@app.cell
def _(mo, table):
    mo.md(f"Selected rows: {table.selected_rows}")
    return


if __name__ == "__main__":
    app.run()
