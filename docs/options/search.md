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

# Search

The [search option](https://datatables.net/reference/option/search) let you control the initial value for the search field, and whether the query should be treated as a regular expression or not:

```{code-cell} ipython3
import itables

itables.init_notebook_mode()
```

```{code-cell} ipython3
:tags: [full-width]

df = itables.sample_dfs.get_countries(html=False)
itables.show(df, search={"regex": True, "caseInsensitive": True, "search": "s.ain"})
```
