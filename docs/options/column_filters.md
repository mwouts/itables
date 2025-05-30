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

# Column Filters

Use `column_filters = "header"` or `"footer"` if you wish to display individual column filters
(remove the global search box with a [`layout`](layout) modifier if desired).

```{code-cell} ipython3
import pandas as pd

import itables

itables.init_notebook_mode()

alpha_numeric_df = pd.DataFrame(
    [["one", 1.5], ["two", 2.3]], columns=["string", "numeric"]
)

itables.show(alpha_numeric_df, column_filters="header", layout={"topEnd": None})
```

As always you can set activate column filters by default with e.g.

```{code-cell} ipython3
itables.options.column_filters = "footer"
```

Column filters also work on dataframes with multiindex columns:

```{code-cell} ipython3
itables.sample_dfs.get_dict_of_test_dfs()["multiindex"]
```

```{code-cell} ipython3
:tags: [remove-cell]

# Revert back to the default to avoid interactions with the tests
itables.options.column_filters = False
```
