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

# Search Builder

[SearchBuilder](https://datatables.net/extensions/searchbuilder/) let you build complex search queries. You just need to add it to the layout
by passing e.g. `layout={"top1": "searchBuilder"}`.

It is possible to set a predefined search, as we do in the below:

```{code-cell} ipython3
:tags: [full-width]

import itables

itables.init_notebook_mode()

df = itables.sample_dfs.get_countries(html=False, climate_zone=True)

itables.show(
    df,
    layout={"top1": "searchBuilder"},
    searchBuilder={
        "preDefined": {
            "criteria": [
                {"data": "climate_zone", "condition": "=", "value": ["Sub-tropical"]}
            ]
        }
    },
)
```
