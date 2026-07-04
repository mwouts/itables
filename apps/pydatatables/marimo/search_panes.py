import marimo

__generated_with = "0.13.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    from pydatatables.sample_dfs import get_countries
    from pydatatables.widget import DataTable

    mo.output.append(
        DataTable(
            get_countries(climate_zone=True).reset_index(),
            layout={"top1": "searchPanes"},
            searchPanes={
                "layout": "columns-3",
                "cascadePanes": True,
                "columns": [1, 6, 7],
            },
        )
    )
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
