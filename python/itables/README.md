# itables: Python DataFrames as interactive DataTables

Starting with v3, the [ITables](https://github.com/mwouts/itables) project
is made of three packages:

- [`pydatatables`](https://pypi.org/project/pydatatables/) renders Python DataFrames using [DataTables](https://datatables.net/)
- [`pyaggrid`](https://pypi.org/project/pyaggrid/) renders Python DataFrames using [AG Grid](https://www.ag-grid.com/)
- `itables_core` contains the functions shared by the two renderers (downsampling, formatting, ...)

The `itables` package itself is now a thin backward-compatibility wrapper around
`pydatatables`: the historical itables API keeps working unchanged, e.g.

```python
from itables import init_notebook_mode, show

init_notebook_mode(all_interactive=True)
```

as well as `itables.options`, `from itables.widget import ITable`,
`from itables.dash import ITable`, `from itables.streamlit import interactive_table`,
`from itables.shiny import DT`, `itables.typing.ITableOptions`, etc.

New projects should prefer `pydatatables` (or `pyaggrid`) directly.

Note: the configuration file is now named `pydatatables.toml` (was `itables.toml`),
the `pyproject.toml` section is `[tool.pydatatables]` (was `[tool.itables]`), and
the environment variables are `PYDATATABLES_CONFIG` and
`PYDATATABLES_CEILING_DIRECTORIES`.

## Documentation

Browse the [documentation](https://mwouts.github.io/itables/) to see
examples of Pandas or Polars DataFrames rendered as interactive DataTables.
