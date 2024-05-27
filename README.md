![ITables logo](https://raw.githubusercontent.com/mwouts/itables/3f8e8bd75af7ad38a500518fcb4fbbc370ea6c4c/itables/logo/wide.svg)

![CI](https://github.com/mwouts/itables/actions/workflows/continuous-integration.yml/badge.svg?branch=main)
[![codecov.io](https://codecov.io/github/mwouts/itables/coverage.svg?branch=main)](https://codecov.io/github/mwouts/itables?branch=main)
[![Pypi](https://img.shields.io/pypi/v/itables.svg)](https://pypi.python.org/pypi/itables)
[![Conda Version](https://img.shields.io/conda/vn/conda-forge/itables.svg)](https://anaconda.org/conda-forge/itables)
[![pyversions](https://img.shields.io/pypi/pyversions/itables.svg)](https://pypi.python.org/pypi/itables)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

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
from itables import init_notebook_mode

init_notebook_mode(all_interactive=True)
```
and then render any DataFrame as an interactive table that you can sort, search and explore:
![df](docs/df_example.png)

If you prefer to render only selected DataFrames as interactive tables, use `itables.show` to show just one Series or DataFrame as an interactive table:
![show](docs/show_df.png)

Since `itables==1.0.0`, the [jQuery](https://jquery.com/) and [DataTables](https://datatables.net/) libraries and CSS
are injected in the notebook when you execute `init_notebook_mode` with its default argument `connected=False`.
Thanks to this the interactive tables will work even without a connection to the internet.

If you prefer to load the libraries dynamically (and keep the notebook lighter), use `connected=True` when you
execute `init_notebook_mode`.

## Supported environments

ITables works in all the usual Jupyter Notebook environments, including Jupyter Notebook, Jupyter Lab, Jupyter nbconvert (i.e. the tables are still interactive in the HTML export of a notebook), Jupyter Book, Google Colab and Kaggle.

You can also use ITables in [Quarto](https://mwouts.github.io/itables/quarto.html) HTML documents, and in RISE presentations.

ITables works well in VS Code, both in Jupyter Notebooks and in interactive Python sessions.

Last but not least, ITables is also available in
[Streamlit](https://mwouts.github.io/itables/streamlit.html) or
[Shiny](https://mwouts.github.io/itables/shiny.html) applications.
