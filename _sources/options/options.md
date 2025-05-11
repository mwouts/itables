---
jupytext:
  formats: md:myst
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

# Options

## DataTable Options

ITables is a wrapper for the Javascript DataTables library, which means that you can use more or less directly the DataTables [options](https://datatables.net/options) from within Python.

Since ITables just maps these options to DataTables, you are invited to have a look at DataTable's great [documentation](https://datatables.net/), and to its huge collection of [examples](https://datatables.net/examples/index). The DataTable [forum](https://datatables.net/forums/) can be quite useful as well.

A non-exhaustive list of the DataTable options, together with their expected types, is available at [`itables.typing.DataTableOptions`](https://github.com/mwouts/itables/blob/main/src/itables/typing.py). If you see an option that you find useful, please make a PR (and add an example to the documentation, too).

```{code-cell} ipython3
:tags: [scroll-output]

import inspect

import itables

print(inspect.getsource(itables.typing.DataTableOptions))
```

## ITable Options

ITables itself adds a few options like `connected`, `maxBytes`, `allow_html` etc.

The ITable options are documented at [`itables.typing.ITableOptions`](https://github.com/mwouts/itables/blob/main/src/itables/typing.py):

```{code-cell} ipython3
:tags: [scroll-output]

print(inspect.getsource(itables.typing.ITableOptions))
```

## Default values

Some of the options have a default value set in [`itables.options`](https://github.com/mwouts/itables/blob/main/src/itables/options.py). You can change these defaults easily, and even set defauts for the options that don't have one yet with e.g.

```python
import itables

itables.options.maxBytes = "128KB"
```

```{code-cell} ipython3
:tags: [scroll-output]

print(inspect.getsource(itables.options))
```
