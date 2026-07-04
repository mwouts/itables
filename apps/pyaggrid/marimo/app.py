import marimo

__generated_with = "0.13.6"
app = marimo.App()


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Using pyaggrid in Marimo

    pyaggrid does not have a native Marimo widget yet, however you can
    use `to_html_aggrid` in combination with `mo.iframe` to display a
    DataFrame as an AG Grid table. An internet connection is required
    as AG Grid is loaded from a CDN.
    """)
    return


@app.cell
def _():
    import marimo as mo
    from itables_core.sample_dfs import get_dict_of_test_dfs
    from pyaggrid import to_html_aggrid

    df = get_dict_of_test_dfs()["int_float_str"]

    html = to_html_aggrid(df)
    mo.iframe(html)
    return


if __name__ == "__main__":
    app.run()
