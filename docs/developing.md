# Developing ITables

In this page you will find instructions on how to
create a development environment and how
to test your changes.

## How to create a development environment

Create a conda environment with
```shell
mamba env create --file environment.yml
```
(use `conda` if you don't have `mamba`) or update it with
```shell
mamba env update --file environment.yml
```

Then, activate that environment with
```shell
conda activate itables
```

Install the pre-commit hooks with
```shell
pre-commit install
```

and finally, install the development version of `itables` with
```shell
pip install -e .
```

## How to run the Python test suite

The Python code can be tested with just

```shell
pytest
```

Running the `pytest` test suite is not enough to guaranty that a change won't
break `itables`. You also need to test that the tables are well rendered in the
different contexts like Jupyter Book, Jupyter Lab, VS Code.

## Jupyter Book

The `itables` documentation uses [Jupyter Book](https://jupyterbook.org/).

To build the documentation locally,
you need to create a Jupyter kernel named `itables` with
```shell
python -m ipykernel install --name itables --user
```
Then you can build the documentation with
```
jupyter-book build docs
```

This will give you a link to a local version of the documentation.

If you make any significant change then you should go through
the updated documentation and make sure all the examples
still work properly.

## Jupyter Lab

In the `itables` conda environment, you can start Jupyter with
```
jupyter lab
```

You should test at least this code snippet:
```python
from itables import init_notebook_mode
from itables.sample_dfs import get_countries

# try both connected=False (the default) and connected=True
init_notebook_mode(all_interactive=True, connected=False)

get_countries()
```

You can do this using for instance the notebook at `tests/test_notebook.ipynb`.

Note that you can also open the documentation in Jupyter:
go to the `docs` folder and open e.g.
[`advanced_parameters.md`](advanced_parameters.md)
_as a notebook_ (using a right click).

## Other notebook editors

If you change anything related to the Javascript/HTML code,
you should test the [supported editors](supported_editors.md)
in both the connected and offline mode.

For the online editors like [Google Colab](https://colab.research.google.com/),
you might have to install your development version there with e.g.
```
!pip uninstall itables -y
!pip install git+https://github.com/mwouts/itables.git@branch
```
