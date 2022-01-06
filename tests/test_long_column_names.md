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

In this notebook we document an issue with long column names.

```python
import pandas as pd
df = pd.DataFrame({"very " * 5 + "long name": [0] * 5,
              "very " * 10 + "long name": [1] * 5,
              "very " * 20 + "long name": [2] * 5,
              "nospacein" + "very" * 50 + "longname": [3] * 5,
              "nospacein" + "very" * 100 + "longname": [3] * 5})
```

In Pandas the long names result in a very wide HTML table, however the columns don't overlap.

```python
df
```

With `datatables.net` the column width are fixed and because of this the columns do overlap. Note that, with the default `display` class, the columns that contains spaces are wrapped.

```python
from itables import init_notebook_mode, show
init_notebook_mode()
show(df)
```

Maybe we can use the `columnDefs` argument to create wider columns?
```python
show(df, columnDefs = [{"width": "500px", "targets": "_all"}])
```

Or use the `autoWidth` argument (but I see no change here)?
```python
show(df, autoWidth = True)
```
