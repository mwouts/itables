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

# Show dtypes

By default, the columns dtypes are shown only for Polars dataframes. If you prefer, you can change the value of `show_dtypes` to either `True` or `False` to always or never show the index (the default value being `"auto"`).

```{code-cell} ipython3
import itables

itables.init_notebook_mode()
```

You can change this behavior globally with e.g.
```python
itables.options.show_dtypes = True
```

or locally by passing an argument `show_dtypes` to the `show` function:

```{code-cell} ipython3
itables.show(itables.sample_dfs.get_countries(), show_dtypes=True)
```
