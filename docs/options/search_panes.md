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

# Search Panes

[SearchPanes](https://datatables.net/extensions/searchpanes/) is an extension that lets you select rows based on unique values. In the example below we have activated the cascade filtering through the [`searchPanes.cascadePanes`](https://datatables.net/extensions/searchpanes/examples/initialisation/cascadePanes.html) argument.

Note that, in Jupyter, the [`searchPanes.layout`](https://datatables.net/extensions/searchpanes/layout) argument is required (otherwise the search panes are too wide).

```{code-cell} ipython3
:tags: [full-width]

import itables

itables.init_notebook_mode()

df = itables.sample_dfs.get_countries(html=False, climate_zone=True)

itables.show(
    df.reset_index(),
    layout={"top1": "searchPanes"},
    searchPanes={"layout": "columns-3", "cascadePanes": True, "columns": [1, 6, 7]},
)
```

```{warning}
When searching, please keep in mind that ITables will [downsample](../downsampling.md) your table if it is larger than `maxBytes`, so you might not see the full dataset - pay attention to the downsampling message at the bottom left of the table.
```
