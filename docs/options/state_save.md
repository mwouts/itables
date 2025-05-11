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

# State Save

To preserve the table state, like the [selected columns](colvis.md) or the [row order](order.md) you can use the [`stateSave`](https://datatables.net/reference/option/stateSave) option. This will preserve the table state when the page is reloaded, or when an ITable component is updated.

```{tip}
You might also want to adjust [`stateDuration`](https://datatables.net/reference/option/stateDuration) which defaults to 2 hours.
```

Try the option on this page: re-order the table by clicking on one column, then refresh the page - the order will be preserved.

```{code-cell} ipython3
:tags: [full-width]

import itables

itables.init_notebook_mode()

df = itables.sample_dfs.get_countries(html=False)

itables.show(df, stateSave=True)
```
