import marimo

__generated_with = "0.13.6"
app = marimo.App()


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    # Using the ITable HTML representation in Marimo

    The `show` method of ITables does not work in Marimo. We recommend
    that you use the `ITable` widget instead.

    However you can also use the `to_html_datatable` method in combination
    with `mo.iframe` to display a table in Marimo. You need to pass
    `connected=True` as the HTML snippet is not able to access the `init_notebook_mode` cell.
    """
    )
    return


@app.cell
def _():
    import marimo as mo

    from itables import to_html_datatable
    from itables.sample_dfs import get_dict_of_test_dfs

    df = get_dict_of_test_dfs()["int_float_str"]

    html = to_html_datatable(df, selected_rows=[0, 2, 5], select=True, connected=True)
    mo.iframe(html)


if __name__ == "__main__":
    app.run()
