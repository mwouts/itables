# pyaggrid: Python DataFrames as interactive AG Grid tables

`pyaggrid` is part of the [ITables](https://github.com/mwouts/itables) project.
It renders Pandas and Polars DataFrames (and, through
[Narwhals](https://narwhals-dev.github.io/narwhals/), many other DataFrame types)
as interactive [AG Grid](https://www.ag-grid.com/) tables in Python notebooks.

`pyaggrid` shares its core functions (downsampling, formatting) with
[`pydatatables`](https://pypi.org/project/pydatatables/) - the
[DataTables](https://datatables.net/) renderer of the ITables project -
through the `itables_core` package.

## Quick start

Install `pyaggrid` with

```shell
pip install pyaggrid
```

then, in a notebook, run

```python
from pyaggrid import init_notebook_mode, show

init_notebook_mode(all_interactive=True)
```

and your Pandas and Polars DataFrames will be rendered as AG Grid tables.
You can also render a single dataframe with `show(df)`, or get its HTML
representation with `to_html_aggrid(df)`.

The `show` and `to_html_aggrid` functions accept the
[AG Grid options](https://www.ag-grid.com/javascript-data-grid/grid-options/),
e.g. `show(df, rowSelection={"mode": "multiRow"})`, plus a few
pyaggrid-specific options like `theme`, `maxBytes`, `showIndex`... - see
`pyaggrid.typing.PyAgGridOptions`. The default values of these options can
be changed in `pyaggrid.options`.

Large tables are downsampled to `maxBytes` (64KB by default) before being
rendered, exactly like in `pydatatables`.

## Notes

- `pyaggrid` loads AG Grid Community from the URL set in
  `pyaggrid.options.ag_grid_url` (jsDelivr by default). An offline mode
  similar to the one of `pydatatables` is not available yet.
- The rows passed to AG Grid are arrays, not objects. The generated column
  definitions use a `valueGetter` and a `colId` equal to `"c" + column_index`.
  If you pass your own `columnDefs`, they replace the generated ones, so use
  e.g. `valueGetter: params => params.data[0]` (wrapped in a
  `JavascriptFunction`) to access the first column.
