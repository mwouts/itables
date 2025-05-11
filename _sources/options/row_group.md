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

# RowGroup

Use the [RowGroup](https://datatables.net/extensions/rowgroup/) extension to group
the data according to the content of one colum. Optionally, you can hide the content of that column to avoid duplicating the information.

```{code-cell} ipython3
:tags: [full-width]

import itables

itables.init_notebook_mode()

df = itables.sample_dfs.get_countries(html=False)

itables.show(
    df.sort_values("region"),
    rowGroup={"dataSrc": 1},
    columnDefs=[{"targets": 1, "visible": False}],
)
```
