# itables_core

This package contains the core functions shared by the
[ITables](https://github.com/mwouts/itables) rendering packages:

- [`pydatatables`](https://pypi.org/project/pydatatables/) renders Python DataFrames using [DataTables](https://datatables.net/)
- [`pyaggrid`](https://pypi.org/project/pyaggrid/) renders Python DataFrames using [AG Grid](https://www.ag-grid.com/)

It provides, among other things:

- `itables_core.downsample`: downsample a DataFrame to fit `maxRows`/`maxColumns`/`maxBytes` limits
- `itables_core.formatting`: serialize the table content to JSON, with support for
  Pandas, Polars and Narwhals-compatible DataFrames
- `itables_core.typing`: dataframe typing helpers and option-checking utilities
- `itables_core.sample_dfs`: the sample dataframes used in the documentation and tests

You are not expected to install this package directly - it is a dependency
of `pydatatables` and `pyaggrid`.
