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

# Horizontal Scroll

DataTables has a [`scrollX`](https://datatables.net/reference/option/scrollX) option that might be helpful for wide tables.

```{tip}
Since ITables v2.1.2, the `.dt-layout-table` div has a default overflow equal to `auto`, so in most cases you don't need to use `scrollX`.
```

```{code-cell} ipython3
:tags: [full-width]

import itables

itables.init_notebook_mode()

df = itables.sample_dfs.get_dict_of_test_dfs()["wide"]
itables.show(df, scrollX=True)
```

```{warning}
Using `scrollX` on a table that is not wide enough can lead to an issue where the table headers are not aligned with the table content.
```
