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
conda activate itables-dev
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

To build the documentation locally, use
```
jupyter-book build docs
```
