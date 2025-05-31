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

# FixedColumns

[FixedColumn](https://datatables.net/extensions/fixedcolumns/) is an extension
that let you fix some columns as you scroll horizontally.

```{code-cell} ipython3
import string

import numpy as np
import pandas as pd

import itables

itables.init_notebook_mode()

wide_df = pd.DataFrame(
    {
        letter: np.random.normal(size=100)
        for letter in string.ascii_lowercase + string.ascii_uppercase
    }
)

itables.show(
    wide_df,
    fixedColumns={"start": 1, "end": 2},
    scrollX=True,
)
```
