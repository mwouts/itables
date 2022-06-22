# Supported Notebook Editors

`itables` has been tested in many development environments.

## Jupyter Notebook

Try it on [![Notebook](https://img.shields.io/badge/Binder-JupyterNotebook-blue.svg)](https://mybinder.org/v2/gh/mwouts/itables/main?filepath=docs/quick_start.md)

![](images/notebook.png)

## Jupyter Lab

Try it on [![Lab](https://img.shields.io/badge/Binder-JupyterLab-blue.svg)](https://mybinder.org/v2/gh/mwouts/itables/main?urlpath=lab/tree/docs/quick_start.md)

![](images/lab.png)

## Jupyter NB convert

The tables are still interactive when you _download_ the notebook as an HTML file, or when you execute `jupyter nbconvert --to html`.

![](images/html.png)

## Jupyter Book

The tables are interactive in interactive books powered by [Jupyter Book](https://jupyterbook.org), see e.g. the [ITables documentation](https://mwouts.github.io/itables/).

## Google Colab

A short sample notebook is available [here](https://colab.research.google.com/drive/1JPZIasTiH3rIUysDr3eWDz4jgTTq00aq?usp=sharing)

![](images/colab.png)

## VS Code

In VS Code, `itables` works both for Jupyter Notebooks and Python scripts

![](images/code.png)

## PyCharm

In PyCharm we recommend to call `init_notebook_mode` with the `connected=True` argument,
because otherwise the notebooks do not display the interactive tables when they are reloaded.

![](images/pycharm.png)
