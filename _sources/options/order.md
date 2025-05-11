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

Since `itables>=1.3.0`, the interactive datatable shows the rows in the same order as the original dataframe:

```{code-cell} ipython3
import pandas as pd

import itables

itables.init_notebook_mode()

for name, test_df in itables.sample_dfs.get_dict_of_test_dfs().items():
    if "sorted" in name:
        itables.show(test_df, caption=name.replace("_", " ").title())
```

You can also set an explicit [`order`](https://datatables.net/reference/option/order) argument:

```{code-cell} ipython3
sorted_df = pd.DataFrame({"i": [1, 2], "a": [2, 1]}).set_index(["i"])
itables.show(sorted_df, order=[[1, "asc"]])
```
