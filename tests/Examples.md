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

## A sample HTML table

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

```python
from itables import show
show(df)
```

```python
show(df_complex_index)
```

## Using itables for all tables

```python
from itables import init_itables
init_itables()
```

```python
df
```

# Advanced formatting

## Change column width for one column

```python
# Enlarge column 'name', and remove 'nowrap' in classes
show(df, columnDefs= [{"width": "200px", "targets": 4}], classes='display')
```

```python
show(df.T, columnDefs = [{ "width": "50px", "targets": "_all" }])
```

## Printing a table with many columns

The table looks better when we set a minimal width on columns...

```python
show(df.T, columnDefs = [{ "width": "50px", "targets": "_all" }])
```

## Custom paging

We can ask to show as little as 2 entries per page...

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

## Global configuration

*TODO!!*


# Other interactive tables


## QGrid by Quantopian

Is great!
And yes, we can filter on the column content.

```python
import qgrid
qgrid.show_grid(df)
```

## IPyAggrid

The underlying ag-grid javascript library looks great!

```python
from ipyaggrid import Grid

Grid(grid_data=df,
     grid_options = {'columnDefs' : [{'field': c} for c in df.columns]})
```

## IPySheet

I still have to find out how to print a dataframe.

```python
import ipysheet
ipysheet.sheet()
```
