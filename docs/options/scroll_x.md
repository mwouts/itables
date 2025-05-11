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

# Horizontal Scroll

Since ITables 2.1.2, the `.dt-layout-table` div has a default overflow equal to `auto`, so in most cases you don't need to use the [`scrollX`](https://datatables.net/reference/option/scrollX) option of datatables.

```{code-cell} ipython3
:tags: [full-width]

import itables

itables.init_notebook_mode()

df = itables.sample_dfs.get_countries(html=False)
itables.show(df, scrollX=True)
```
