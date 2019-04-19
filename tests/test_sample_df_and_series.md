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
from sample_tables import sample_series, sample_tables, table_with_complex_header
```

# Sample tables

```python
for df in sample_tables():
    show(df)
```

# Table with complex header

```python
show(table_with_complex_header())
```

# Series

```python
for x in sample_series():
    show(x)
```
