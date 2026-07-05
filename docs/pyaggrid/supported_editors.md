# Supported Editors

PyAgGrid generates plain HTML snippets that load AG Grid as an ES module,
so it works in the same environments as `pydatatables` - with the
difference that `show` requires an internet connection (the widget, Dash
and Streamlit components come with their own copy of AG Grid and work
offline).

## Jupyter Notebook and Jupyter Lab

Both `init_notebook_mode` and `show` work in Jupyter. Try it on
[![Lab](https://img.shields.io/badge/Binder-JupyterLab-blue.svg)](https://mybinder.org/v2/gh/mwouts/itables/main?urlpath=lab/tree/docs/pyaggrid/index.md)

## Jupyter NB convert

The tables are still interactive when you _download_ the notebook as an HTML file, or when you execute `jupyter nbconvert --to html`.

## Jupyter Book

The tables are interactive in interactive books powered by [Jupyter Book](https://jupyterbook.org) - like this documentation.

## Google Colab

Google Colab encapsulates the outputs in iframes, so every table loads
AG Grid from the internet - which is what PyAgGrid does anyway.

## VS Code

In VS Code, `pyaggrid` works both for Jupyter Notebooks and Python scripts.

## Marimo, Dash, Streamlit, Shiny

See the corresponding pages in the "Using PyAgGrid" section.
