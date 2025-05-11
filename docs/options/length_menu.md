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

# LengthMenu

Select [how many entries](https://datatables.net/examples/advanced_init/length_menu.html) should appear at once in the table with either the `lengthMenu` argument of the `show` function, or with the global option `itables.options.lengthMenu`:

```{code-cell} ipython3
import itables

itables.init_notebook_mode()
df = itables.sample_dfs.get_countries(html=False)
```

```{code-cell} ipython3
:tags: [full-width]

itables.show(df, lengthMenu=[2, 5, 10, 20, 50])
```
