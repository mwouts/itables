---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.13.5
  kernelspec:
    display_name: itables
    language: python
    name: itables
---

In this notebook we display a dataframe with very long column names.

```python
import pandas as pd
df = pd.DataFrame({"short name": [0] * 5,
                   "very " * 5 + "long name": [0] * 5,
              "very " * 10 + "long name": [1] * 5,
              "very " * 20 + "long name": [2] * 5,
              "nospacein" + "very" * 50 + "longname": [3] * 5,
              "nospacein" + "very" * 100 + "longname": [3] * 5})
```

In Pandas the long names result in a very wide HTML table, however the columns don't overlap.

```python
df
```

With `datatables.net` the column width are fixed and because of this the columns did overlap when the style of `table th` was not set (issue #28). Note that, with the default `display` class, long columns names made of multiple words are wrapped onto multiple lines.

```python
from itables import init_notebook_mode, show
init_notebook_mode()
show(df)
```
