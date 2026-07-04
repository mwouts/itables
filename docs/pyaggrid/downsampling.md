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

# ruff: noqa: E402
# pyright: reportUnusedExpression=false
```

# Downsampling

When an interactive table is displayed by `pyaggrid`, the table data is embedded into the notebook itself. Large tables need to be downsampled, otherwise your notebook will become huge and unresponsive.

Downsampling occurs when the table data is larger than `maxBytes`, which is equal to 64KB by default. When downsampling occurs, a warning is displayed below the table.

If you wish, you can increase the value of `maxBytes` or even deactivate the limit (with `maxBytes=0`) - but again, that will break your notebook when you display a large dataframe.

Similarly, you can set a limit on the number of rows (`maxRows`, defaults to 0) or columns (`maxColumns`, defaults to `200`).

The downsampling is implemented in the `itables_core` package and is
shared with `pydatatables`.

```{code-cell} ipython3
import itables_core.downsample
import itables_core.sample_dfs
import pyaggrid

pyaggrid.init_notebook_mode()
```

```{code-cell} ipython3
:tags: [full-width]

pyaggrid.options.maxBytes = "8KB"

df = itables_core.sample_dfs.get_countries()
(
    itables_core.downsample.as_nbytes(pyaggrid.options.maxBytes),
    itables_core.downsample.nbytes(df),
)
```

```{code-cell} ipython3
:tags: [full-width]

df
```

To show the table in full, we can modify the value of `maxBytes` either locally:

```{code-cell} ipython3
:tags: [full-width]

pyaggrid.show(df, maxBytes=32768)
```

or globally:

```{code-cell} ipython3
:tags: [full-width]

pyaggrid.options.maxBytes = "1MB"
df
```

```{code-cell} ipython3
:tags: [remove-cell]

pyaggrid.options.maxBytes = "64KB"
pyaggrid.init_notebook_mode(all_interactive=False)
```
