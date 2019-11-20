# Pandas DataFrame

```python
import world_bank_data as wb

df = wb.get_countries()
df = df.loc[df.region!="Aggregates"]
df
```

# Make it interactive
(Search Brazil)

```python
import itables.interactive
df
```

# Pagination
(Sort by latitude)

```python
from itables import show
show(df, scrollY="300px", scrollCollapse=True, paging=False)
```

# DataTables.net

Great library, well documented at https://datatables.net/reference/. Copy paste the Javascript examples here!

```python
import pandas as pd
show(
    pd.DataFrame([[-1, 2, -3, 4, -5], [6, -7, 8, -9, 10]], columns=list("abcde")),
    columnDefs=[
        {
            "targets": "_all",
            "createdCell": """function (td, cellData, rowData, row, col) {
      if ( cellData < 0 ) {
        $(td).css('color', 'red')
      }
    }""",
        }
    ],
)
```
<div style="font-size: 18px">

# What works

- Interative tables in Jupyter Notebook
- Copy paste from the DataTables documentation
- HTML export as simple as `jupyter nbconvert --to html`
- Automatic downsampling of large tables

# Please help

- Make this happen in Jupyter Lab
- And in Plotly Dash
- Offline mode?
- Should we extend this to ag-grid, react-table, or to your favorite interactive table?
