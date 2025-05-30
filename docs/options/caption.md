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

# Caption

```{code-cell} ipython3
:tags: [full-width]

import itables

itables.init_notebook_mode()

df = itables.sample_dfs.get_countries(html=False)
itables.show(df, "Countries from the World Bank Database")
```

The caption appears at the bottom of the table by default: this is governed by `caption-side:bottom`
in the [`style` option](style) (but for some reason this is not effective in Jupyter Book 🤔).
