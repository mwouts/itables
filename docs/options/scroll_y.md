---
jupytext:
  formats: docs///md:myst,docs/py///py:percent
  notebook_metadata_filter: -jupytext.text_representation.jupytext_version
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
kernelspec:
  display_name: python3
  language: python
  name: python3
---

# Vertical Scroll

The [`scrollY`](https://datatables.net/examples/basic_init/scroll_y.html) parameter is an interesting alternative to the pagination:

```{code-cell} ipython3
:tags: [full-width]

import itables

itables.init_notebook_mode()

df = itables.sample_dfs.get_countries()
itables.show(df, scrollY="350px", scrollCollapse=True, paging=False)
```

## Scroller

```{versionadded} 2.8.1
```

When `scrollY` is set, DataTables still renders every row of the current page into the
page (and with `paging=False`, every row of the table). That is fine for small tables,
but for large ones it is more efficient to render only the rows that are actually
visible. This is what the [Scroller](https://datatables.net/extensions/scroller/)
extension does: it implements *virtual scrolling*, so only the rows in (or near) the
viewport exist in the DOM at any given time, while the scrollbar still represents the
full table.

To enable it, set `scroller=True` together with `scrollY`:

```{code-cell} ipython3
:tags: [full-width]

itables.show(df, scroller=True, scrollY="350px")
```

### Defer Render

The `deferRender` option tells DataTables to only create the HTML for a row when it is
first displayed. It pairs naturally with Scroller and further reduces the initial
rendering cost for large tables:

```{code-cell} ipython3
:tags: [full-width]

itables.show(df, scroller=True, scrollY="350px", deferRender=True)
```

### Scroller options

You can pass a dictionary to `scroller` to configure it further. For example,
`loadingIndicator=True` shows a message while rows are being rendered:

```{code-cell} ipython3
:tags: [full-width]

itables.show(df, scroller={"loadingIndicator": True}, scrollY="350px", deferRender=True)
```

As always, you can set these options globally with:
```python
itables.options.scroller = True
itables.options.deferRender = True
```

or by adding
```
scroller = true
deferRender = true
```
to your [`itables.toml` configuration file](../configuration.md).
