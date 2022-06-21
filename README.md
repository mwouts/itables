# Interactive Tables

[![Pypi](https://img.shields.io/pypi/v/itables.svg)](https://pypi.python.org/pypi/itables)
![CI](https://github.com/mwouts/itables/workflows/CI/badge.svg)
[![codecov.io](https://codecov.io/github/mwouts/itables/coverage.svg?branch=main)](https://codecov.io/github/mwouts/itables?branch=main)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/mwouts/itables.svg)](https://lgtm.com/projects/g/mwouts/itables/context:python)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Pandas DataFrames and Series as interactive [datatables](https://datatables.net)!

Install the package with
```
pip install itables
```

Activate the interactive mode for all series and dataframes with
```python
from itables import init_notebook_mode
init_notebook_mode(all_interactive=True)
```
or use `itables.show` to show just one Series or DataFrame as an interactive table.

(NB: In Jupyter Notebook, Jupyter NBconvert and Jupyter Book, you need to call `init_notebook_mode()` before using `show`).

## Documentation

Read more about `itables` and advanced use cases in the [documentation](https://mwouts.github.io/itables/).

In particular, the `show` method let you pass custom parameters to [datatables.net](https://datatables.net/)'s `DataTable()`'s constructor - see the [advanced parameters examples](advanced_parameters.md).

## Supported environments

`itables` has been tested in the following editors:
- Jupyter Notebook
- Jupyter Lab
- Jupyter nbconvert (i.e. the tables are still interactive in the HTML export of a notebook)
- Jupyter Book
- Google Colab
- VS Code (for both Jupyter Notebooks and Python scripts)
- PyCharm (for Jupyter Notebooks)

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

## <a name="downsampling"></a> Downsampling

When the data in a table is larger than `maxBytes`, which is equal to 64KB by default, `itables` will display only a subset of the table - one that fits into `maxBytes`. If you wish, you can deactivate the limit with `maxBytes=0`, change the value of `maxBytes`, or similarly set a limit on the number of rows (`maxRows`, defaults to 0) or columns (`maxColumns`, defaults to `pd.get_option('display.max_columns')`).

Note that datatables support [server-side processing](https://datatables.net/examples/data_sources/server_side). At a later stage we may implement support for larger tables using this feature.

```{code-cell}
from itables.sample_dfs import get_indicators
import itables.options as opt

opt.lengthMenu = [2, 5, 10, 20, 50, 100, 200, 500]
opt.maxBytes = 10000

df = get_indicators()
df.values.nbytes
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
