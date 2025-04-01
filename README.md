![ITables logo](https://raw.githubusercontent.com/mwouts/itables/3f8e8bd75af7ad38a500518fcb4fbbc370ea6c4c/itables/logo/wide.svg)

[![CI](https://github.com/mwouts/itables/actions/workflows/continuous-integration.yml/badge.svg?branch=main)](https://github.com/mwouts/itables/actions)
[![codecov.io](https://codecov.io/github/mwouts/itables/coverage.svg?branch=main)](https://codecov.io/github/mwouts/itables?branch=main)
[![MIT License](https://img.shields.io/github/license/mwouts/itables)](LICENSE)
[![Pypi](https://img.shields.io/pypi/v/itables.svg)](https://pypi.python.org/pypi/itables)
[![Conda Version](https://img.shields.io/conda/vn/conda-forge/itables.svg)](https://anaconda.org/conda-forge/itables)
[![pyversions](https://img.shields.io/pypi/pyversions/itables.svg)](https://pypi.python.org/pypi/itables)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Jupyter Widget](https://img.shields.io/badge/Jupyter-Widget-F37626.svg?style=flat&logo=Jupyter)](https://mwouts.github.io/itables/widget.html)
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_red.svg)](https://itables.streamlit.app)

This packages changes how Pandas and Polars DataFrames are rendered in Jupyter Notebooks.
With `itables` you can display your tables as interactive [DataTables](https://datatables.net/)
that you can sort, paginate, scroll or filter.

ITables is just about how tables are displayed. You can turn it on and off in just two lines,
with no other impact on your data workflow.

The `itables` package only depends on `numpy`, `pandas` and `IPython`
which you must already have if you work with Pandas in Jupyter (add `polars`, `pyarrow` if you
work with Polars DataFrames).

## Documentation

Browse the [documentation](https://mwouts.github.io/itables/) to see
examples of Pandas or Polars DataFrames rendered as interactive DataTables.

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
import itables

itables.init_notebook_mode()
```
and then render any DataFrame as an interactive table that you can sort, search and explore:
![df](docs/df_example.png)

If you prefer to render only selected DataFrames as interactive tables, call `itables.init_notebook_mode(all_interactive=False)`, then use `itables.show` to show just one Series or DataFrame as an interactive table:
![show](docs/show_df.png)

Since ITables v1.0, the [jQuery](https://jquery.com/) and [DataTables](https://datatables.net/) libraries and CSS
are injected in the notebook when you execute `init_notebook_mode` with its default argument `connected=False`.
Thanks to this the interactive tables will work even without a connection to the internet.

If you prefer to load the libraries dynamically (and keep the notebook lighter), use `connected=True` when you
execute `init_notebook_mode`.

## Supported notebook environments

ITables works in all the usual Jupyter Notebook environments, including Jupyter Notebook, Jupyter Lab, Jupyter nbconvert (i.e. the tables are still interactive in the HTML export of a notebook), Jupyter Book, Google Colab and Kaggle.

You can also use ITables in [Quarto](https://mwouts.github.io/itables/quarto.html) HTML documents, and in RISE presentations.

ITables works well in VS Code, both in Jupyter Notebooks and in interactive Python sessions.

## ITables in Python applications

Last but not least, ITables is also available as
- a [Jupyter Widget](https://mwouts.github.io/itables/widget.html)
- a [Dash](https://mwouts.github.io/itables/dash.html) component
- a [Streamlit](https://mwouts.github.io/itables/streamlit.html) component,
- and it also works in [Shiny](https://mwouts.github.io/itables/shiny.html) applications.
