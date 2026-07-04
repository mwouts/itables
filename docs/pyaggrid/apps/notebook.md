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

# Notebook Mode

Activate PyAgGrid in a Jupyter environment for all your tables with `init_notebook_mode`:

```{code-cell} ipython3
import pyaggrid

pyaggrid.init_notebook_mode()
```

You can go back to the standard HTML representation of Pandas DataFrames with `init_notebook_mode(all_interactive=False)`.

```{code-cell} ipython3
:tags: [full-width]

import itables_core.sample_dfs

df = itables_core.sample_dfs.get_countries()
df
```

```{warning}
Unlike `pydatatables`, `pyaggrid` does not have an offline mode yet:
the AG Grid library is loaded from the URL set in
`pyaggrid.options.ag_grid_url` (jsDelivr by default), so an internet
connection is required when the tables are displayed.
```

## Show

If you prefer to render only certain tables using `pyaggrid`, or want to set additional options, use `show`:

```{code-cell} ipython3
:tags: [full-width]

pyaggrid.show(df, caption="A DataFrame rendered with PyAgGrid")
```
