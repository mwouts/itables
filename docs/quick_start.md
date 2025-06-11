---
jupytext:
  formats: docs///md:myst,docs/py///py:percent
  notebook_metadata_filter: -jupytext.text_representation.jupytext_version
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
kernelspec:
  display_name: itables
  language: python
  name: itables
---

```{code-cell} ipython3
:tags: [remove-cell]

# pyright: reportUnusedExpression=false
```

![ITables Logo](../src/itables/logo/text.svg)

[![CI](https://github.com/mwouts/itables/actions/workflows/continuous-integration.yml/badge.svg?branch=main)](https://github.com/mwouts/itables/actions)
[![codecov.io](https://codecov.io/github/mwouts/itables/coverage.svg?branch=main)](https://codecov.io/github/mwouts/itables?branch=main)
[![MIT License](https://img.shields.io/github/license/mwouts/itables)](https://github.com/mwouts/itables/blob/main/LICENSE)
[![Pypi](https://img.shields.io/pypi/v/itables.svg)](https://pypi.python.org/pypi/itables)
[![Conda Version](https://img.shields.io/conda/vn/conda-forge/itables.svg)](https://anaconda.org/conda-forge/itables)
[![pyversions](https://img.shields.io/pypi/pyversions/itables.svg)](https://pypi.python.org/pypi/itables)
 ![PyPI - Types](https://img.shields.io/pypi/types/itables)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Jupyter Widget](https://img.shields.io/badge/Jupyter-Widget-F37626.svg?style=flat&logo=Jupyter)](apps/widget.md)
[![Dash Component](https://img.shields.io/badge/Dash-Plotly-1098F7.svg?style=flat&logo=Plotly)](apps/dash.md)
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_red.svg)](https://itables.streamlit.app)
<a class="github-button" href="https://github.com/mwouts/itables" data-icon="octicon-star" data-show-count="true"></a>
<script src="https://buttons.github.io/buttons.js"></script>

This packages changes how Pandas and Polars DataFrames are rendered in Python notebooks and applications.
With `itables` you can display your tables as interactive [DataTables](https://datatables.net/)
that you can sort, paginate, scroll or filter.

ITables is just about how tables are displayed. You can turn it on and off in just two lines,
with no other impact on your data workflow.

The `itables` package depends only on `numpy`, `pandas` and `IPython`
which you must already have if you work with Pandas in Jupyter (add `polars`, `pyarrow` if you
work with Polars DataFrames).

# Quick Start

## Installation

Install the `itables` package with either

```shell
pip install itables
```

or
```shell
conda install itables -c conda-forge
```

## Notebook Mode

In a Jupyter Notebook, activate the interactive mode for all your DataFrames with [`init_notebook_mode`](apps/notebook.md):

```{code-cell} ipython3
import itables

itables.init_notebook_mode()
```

After this, any Pandas or Polars DataFrame, or Series,
is displayed as an interactive [DataTables](https://datatables.net/),
which lets you explore, filter or sort your data.

```{code-cell} ipython3
:tags: [full-width]

df = itables.sample_dfs.get_countries(html=False)
df
```

Read more about the different context where you can use ITables.

## Binder

You can run the examples above (or any other documentation page) directly on ![Lab](https://img.shields.io/badge/Binder-JupyterLab-blue.svg), without having to install anything on your end - just click on the rocket icon at the top of the page.

## Licence

ITables is developed by [Marc Wouts](https://github.com/mwouts) on [GitHub](https://github.com/mwouts/itables),
under a MIT license.

ITables is a wrapper for [datatables.net](https://datatables.net/) which is developed by Allan Jardine
[(sponsor him!)](https://github.com/sponsors/AllanJard), also under a MIT license.
