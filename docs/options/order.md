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

# Order

Since ITables v1.3.0, the interactive datatable shows the rows in the same order as the original dataframe.

You can pre-select a explicit order with the [`order`](https://datatables.net/reference/option/order) option:

```{code-cell} ipython3
import pandas as pd

import itables

itables.init_notebook_mode()

sorted_df = pd.DataFrame({"a": [2, 1]}, index=pd.Index([1, 2], name="i"))
itables.show(sorted_df, order=[[1, "asc"]])
```
