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

# Rendering Mathematical Formulae

To render mathematical contents like equations in your DataFrame (rows or header), use the `render_math` option:

```{code-cell} ipython3
import pandas as pd

import itables

itables.init_notebook_mode()

itables.show(
    pd.DataFrame(
        {
            "$N_{\\text{event}}$": ["$\\alpha$", "$\\beta$", "$\\gamma$"] * 10,
            "Value": [
                "$0.8_{-0.1}^{+0.3}$",
                "$3.2_{-0.4}^{+0.2}$",
                "$-0.1_{-0.5}^{+0.8}$",
            ]
            * 10,
        }
    ),
    render_math=True,
)
```
