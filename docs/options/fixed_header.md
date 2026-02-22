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

# FixedHeader

[FixedHeader](https://datatables.net/extensions/fixedheader/) is a DataTables extension
that keeps the table header visible while scrolling.

Use `fixedHeader=True` to enable a fixed table header:

```{code-cell} ipython3
:tags: [full-width]

import itables

itables.init_notebook_mode()

df = itables.sample_dfs.get_countries()

itables.show(
    df,
    # fixedHeader=True is simpler,
    # but in some contexts, like here in Jupyter Book,
    # we need to account for the other fixed elements
    fixedHeader={"header": True, "headerOffset": 48},
)
```

You can also configure header and footer behavior explicitly, as in the
[header/footer example](https://datatables.net/extensions/fixedheader/examples/options/header_footer.html):

```{code-cell} ipython3
:tags: [full-width]

itables.show(
    df,
    footer=True,
    fixedHeader={"header": True, "footer": True},
)
```

As always, you can set this option globally with:
```python
itables.options.fixedHeader = True
```

or by adding
```
fixedHeader = true
```
to your [`itables.toml` configuration file](../configuration.md).
