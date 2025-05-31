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

# Select Text in Header

The `text_in_header_can_be_selected` option, which defaults to `True`, is provided by ITables since v2.4.0.

With that option set (the default), you can select the text in the table headers. This is useful in the context of data exploration where
you need to copy back the column name to your code.

```{code-cell} ipython3
import itables

itables.init_notebook_mode()
df = itables.sample_dfs.get_countries(html=False)

itables.show(df, "A table in which column headers can be selected")
```

When `text_in_header_can_be_selected=False`, the column title cannot be selected as clicking on the title sorts the table.

```{code-cell} ipython3
itables.show(
    df,
    "A table in which column headers cannot be selected",
    text_in_header_can_be_selected=False,
)
```
