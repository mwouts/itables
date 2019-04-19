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

# From HTML to interactive tables

## Pandas DataFrame as HTML tables

```python
import pandas as pd
import world_bank_data as wb
pd.set_option('display.max_rows', 6)
df = wb.get_countries()
df
```

```python
df_complex_index = df.set_index(['region','name'])
df_complex_index.columns = (pd.DataFrame({'category':['code']*2 +['property']*2 +['localisation']*3}, 
                                        index=df_complex_index.columns.rename('detail'))
            .set_index('category', append=True).swaplevel().index)
df_complex_index
```

## Using itables on one table

Use `show` to display one table.

```python
from itables import show
show(df)
```

```python
show(df_complex_index)
```

## Using itables for all tables

Execute `init_itable_mode` if you want that every dataframe be printed as a javascript table.

```python
from itables import init_itable_mode
init_itable_mode()
```

```python
df
```

## Displaying a series with itables

```python
df.query('region!="Aggregates"').set_index(['region','name']).capitalCity
```

# Advanced formatting

## Change column width for one column

```python
# Columns width not working here?
show(df, columnDefs = [{ "width": "50px", "targets": 4 }], classes=['display', 'nowrap'])
```

## Printing a table with many columns

Tables with many columns look better when we set a minimal width on columns...

```python
show(df.T, columnDefs = [{ "width": "50px", "targets": "_all" }])
```

## Custom paging

We can ask to show as little as 2 entries per page

```python
show(df, lengthMenu = [2, 5, 10, 25, 50, 75, 100 ])
```

## Scroll

```python
show(df, scrollY="200px",scrollCollapse=True, paging=False)
```

## Show table in full

```python
show(df.head(12), paging=False)
```

# Show a large table

```python
wb.get_indicators()
```

```python
wb.get_series('SP.POP.TOTL', mrv=1, simplify_index=True)
```

## Global configuration

*TODO!!*

