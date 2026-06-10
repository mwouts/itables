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

# Col Reorder

[ColReorder](https://datatables.net/extensions/colreorder/) is a DataTables extension
that lets users drag and drop column headers to reorder the table columns interactively.

Use `colReorder=True` to enable column reordering:

```{code-cell} ipython3
:tags: [full-width]

import itables

itables.init_notebook_mode()

df = itables.sample_dfs.get_countries()

itables.show(df, colReorder=True)
```

As always, you can set this option globally with:
```python
itables.options.colReorder = True
```

or by adding
```
colReorder = true
```
to your [`itables.toml` configuration file](../configuration.md).
