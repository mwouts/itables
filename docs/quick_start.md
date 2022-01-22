---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.11.5
kernelspec:
  display_name: itables
  language: python
  name: itables
---

# Interactive Tables

**Pandas DataFrames as Interactive DataTables**

[![Pypi](https://img.shields.io/pypi/v/itables.svg)](https://pypi.python.org/pypi/itables)
![CI](https://github.com/mwouts/itables/workflows/CI/badge.svg)
[![codecov.io](https://codecov.io/github/mwouts/itables/coverage.svg?branch=main)](https://codecov.io/github/mwouts/itables?branch=main)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/mwouts/itables.svg)](https://lgtm.com/projects/g/mwouts/itables/context:python)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
<a class="github-button" href="https://github.com/mwouts/itables" data-icon="octicon-star" data-show-count="true" aria-label="Star mwouts/itables on GitHub">Star</a>
<script async defer src="https://buttons.github.io/buttons.js"></script>

## Quick start

Install the `itables` package with

```shell
pip install itables
```

Activate the interactive mode for all series and dataframes with

```{code-cell} ipython3
from itables import init_notebook_mode

init_notebook_mode(all_interactive=True)
```

After this, any Pandas object (DataFrame or Series) is displayed as an interactive [datatables.net](https://datatables.net/) table, which lets you explore, filter or sort your data.

```{code-cell} ipython3
from itables.sample_dfs import get_countries

df = get_countries()
df
```

If you prefer to render just one series or dataframe as an interactive table, use `show`:

```{code-cell} ipython3
from itables import show
from itables.sample_dfs import get_population

x = get_population()
show(x)
```

(NB: In Jupyter Notebook, Jupyter NBconvert and Jupyter Book, you need to call `init_notebook_mode()` before using `show`).

## Advanced parameters

The `show` method let you pass custom parameters to [datatables.net](https://datatables.net/)'s `DataTable()`'s constructor - see the [advanced parameters examples](advanced_parameters.md).

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
- Or you are offline?

At the moment `itables` does not have an [offline mode](https://github.com/mwouts/itables/issues/8). While the table data is embedded in the notebook, the `jquery` and `datatables.net` are loaded from a CDN, see our [require.config](https://github.com/mwouts/itables/blob/main/itables/javascript/load_datatables_connected.js) and our [table template](https://github.com/mwouts/itables/blob/main/itables/datatables_template.html), so an internet connection is required to display the tables.

## Downsampling

When the data in a table is larger than `maxBytes`, which is equal to 64KB by default, `itables` will display only a subset of the table - one that fits into `maxBytes`. If you wish, you can deactivate the limit with `maxBytes=0`, change the value of `maxBytes`, or similarly set a limit on the number of rows (`maxRows`, defaults to 0) or columns (`maxColumns`, defaults to `pd.get_option('display.max_columns')`).

Note that datatables support [server-side processing](https://datatables.net/examples/data_sources/server_side). At a later stage we may implement support for larger tables using this feature.

```{code-cell} ipython3
from itables.sample_dfs import get_indicators
import itables.options as opt

opt.lengthMenu = [2, 5, 10, 20, 50, 100, 200, 500]
opt.maxBytes = 10000

df = get_indicators()
df.values.nbytes
```

```{code-cell} ipython3
df
```

To show the table in full, we can modify the value of `maxBytes` either locally:

```{code-cell} ipython3
show(df, maxBytes=0)
```

or globally:

```{code-cell} ipython3
opt.maxBytes = 2 ** 20
df
```
