---
jupyter:
  jupytext:
    formats: ipynb,md
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.1'
      jupytext_version: 1.1.1
  kernelspec:
    display_name: Python 3
    language: python
    name: python3
---

```python
from itables import show
from itables.sample import sample_series, sample_dfs
```

# Sample tables

```python
for df in sample_dfs():
    show(df)
```

# Series

```python
for x in sample_series():
    show(x)
```
