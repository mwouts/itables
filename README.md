# Interactive Tables

![CI](https://github.com/mwouts/itables/actions/workflows/continuous-integration.yml/badge.svg?branch=main)
[![codecov.io](https://codecov.io/github/mwouts/itables/coverage.svg?branch=main)](https://codecov.io/github/mwouts/itables?branch=main)
[![Pypi](https://img.shields.io/pypi/v/itables.svg)](https://pypi.python.org/pypi/itables)
[![Conda Version](https://img.shields.io/conda/vn/conda-forge/itables.svg)](https://anaconda.org/conda-forge/itables)
[![pyversions](https://img.shields.io/pypi/pyversions/itables.svg)](https://pypi.python.org/pypi/itables)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Turn your Python DataFrames into Interactive DataTables

This packages changes how Pandas and Polars DataFrames are rendered in Jupyter Notebooks.
With `itables` you can display your tables as interactive [datatables](https://datatables.net/)
that you can sort, paginate, scroll or filter.

ITables is just about how tables are displayed. You can turn it on and off in just two lines,
with no other impact on your data workflow.

The `itables` package only depends on `numpy`, `pandas` and `IPython`
which you must already have if you work with Pandas in Jupyter (add `polars`, `pyarrow` if you
work with Polars DataFrames).

## Documentation

Browse the [documentation](https://mwouts.github.io/itables/) to see
examples of Pandas or Polars DataFrames rendered as interactive datatables.

## Quick start

Install the `itables` package with either
```shell
pip install itables
```

or
```shell
conda install itables -c conda-forge
```

Activate the interactive mode for all series and dataframes with
```python
from itables import init_notebook_mode

init_notebook_mode(all_interactive=True)
```
and then render any DataFrame as an interactive table that you can sort, search and explore:
![df](docs/df_example.png)

If you prefer to render only selected DataFrames as interactive tables, use `itables.show` to show just one Series or DataFrame as an interactive table:
![show](docs/show_df.png)

Since `itables==1.0.0`, the [jquery](https://jquery.com/) and [datatables.net](https://datatables.net/) libraries and CSS
are injected in the notebook when you execute `init_notebook_mode` with its default argument `connected=False`.
Thanks to this the interactive tables will work even without a connection to the internet.

If you prefer to load the libraries dynamically (and keep the notebook lighter), use `connected=True` when you
execute `init_notebook_mode`.

## Supported environments

`itables` has been tested in the following editors:
- Jupyter Notebook
- Jupyter Lab
- Jupyter nbconvert (i.e. the tables are still interactive in the HTML export of a notebook)
- Jupyter Book
- Google Colab
- VS Code (for both Jupyter Notebooks and Python scripts)
- PyCharm (for Jupyter Notebooks)
- Quarto
- Shiny for Python

## Try ITables on Binder

You can run our examples notebooks directly on [![Lab](https://img.shields.io/badge/Binder-JupyterLab-blue.svg)](https://mybinder.org/v2/gh/mwouts/itables/main?urlpath=lab/tree/docs/quick_start.md), without having to install anything on your side.

## Table not loading?

If the table just says "Loading...", then maybe
- You loaded a notebook that is not trusted (run "Trust Notebook" in View / Activate Command Palette)
- You forgot to run `init_notebook_mode`, or you deleted that cell or its output
- Or you ran `init_notebook_mode(connected=True)` but you are not connected to the internet?

Please note that if you change the value of the `connected` argument in
the `init_notebook_mode` cell, you will need to re-execute all the cells
that display interactive tables.

If the above does not help, please check out the [ChangeLog](docs/changelog.md)
and decide whether you should upgrade `itables`.

## <a name="downsampling"></a> Downsampling

When the data in a table is larger than `maxBytes`, which is equal to 64KB by default, `itables` will display only a subset of the table - one that fits into `maxBytes`. If you wish, you can deactivate the limit with `maxBytes=0`, change the value of `maxBytes`, or similarly set a limit on the number of rows (`maxRows`, defaults to 0) or columns (`maxColumns`, defaults to `pd.get_option('display.max_columns')`).

Note that datatables support [server-side processing](https://datatables.net/examples/data_sources/server_side). At a later stage we may implement support for larger tables using this feature.

```{code-cell}
from itables.sample_dfs import get_indicators
from itables.downsample import nbytes
import itables.options as opt

opt.lengthMenu = [2, 5, 10, 20, 50, 100, 200, 500]
opt.maxBytes = 10000

df = get_indicators()
nbytes(df)
```

```{code-cell}
df
```

To show the table in full, we can modify the value of `maxBytes` either locally:

```{code-cell}
show(df, maxBytes=0)
```

or globally:

```{code-cell}
opt.maxBytes = 2 ** 20
df
```
