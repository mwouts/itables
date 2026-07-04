# pydatatables: Python DataFrames as interactive DataTables

`pydatatables` is part of the [ITables](https://github.com/mwouts/itables) project.
It changes how Pandas and Polars DataFrames are rendered in Python notebooks and
applications: with `pydatatables` you can display your tables as interactive
[DataTables](https://datatables.net/) that you can sort, paginate, scroll or filter.

```python
from pydatatables import init_notebook_mode, show

init_notebook_mode(all_interactive=True)
```

If you prefer the [AG Grid](https://www.ag-grid.com/) rendering, use the
[`pyaggrid`](https://pypi.org/project/pyaggrid/) package, which is also developed
in the ITables project and shares the same core functions (downsampling,
formatting) through the `itables_core` package.

Users of the historical `itables` package can keep using it - it is now a thin
wrapper around `pydatatables`.

## Documentation

Browse the [documentation](https://mwouts.github.io/itables/) to see
examples of Pandas or Polars DataFrames rendered as interactive DataTables.
