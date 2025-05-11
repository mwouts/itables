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

# Vertical Scroll

You can replace the pagination with a [vertical scroll](https://datatables.net/examples/basic_init/scroll_y.html):

```{code-cell} ipython3
:tags: [full-width]

import itables

itables.init_notebook_mode()

df = itables.sample_dfs.get_countries(html=False)
itables.show(df, scrollY="200px", scrollCollapse=True, paging=False)
```
