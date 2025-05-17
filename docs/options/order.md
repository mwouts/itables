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

# Order

Since ITables v1.3.0, the interactive datatable shows the rows in the same order as the original dataframe.

You can pre-select a explicit order with the [`order`](https://datatables.net/reference/option/order) option:

```{code-cell} ipython3
import pandas as pd

import itables

itables.init_notebook_mode()

sorted_df = pd.DataFrame({"i": [1, 2], "a": [2, 1]}).set_index(["i"])
itables.show(sorted_df, order=[[1, "asc"]])
```
