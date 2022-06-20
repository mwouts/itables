# Developing ITables

## How to setup a dev environment

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

The test suite can be run with
```shell
pytest
```

## Jupyter Book

The `itables` documentation uses [Jupyter Book](https://jupyterbook.org/).

To build the documentation locally, create a kernel named `itables` with
```shell
python -m ipykernel install --name itables --user
```
and then build the documentation with
```
jupyter-book build docs
```

To publish the documentation to the `gh-pages` branch, use
```shell
ghp-import -n -p -f docs/_build/html
```
