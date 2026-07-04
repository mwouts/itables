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

# Paging

Use [`paging=False`](https://datatables.net/reference/option/paging) to show the table in full:

```{code-cell} ipython3
import itables

itables.init_notebook_mode()
df = itables.sample_dfs.get_countries()
```

```{code-cell} ipython3
:tags: [full-width]

itables.show(df.head(8), paging=False)
```
