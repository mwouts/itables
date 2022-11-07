---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.13.8
kernelspec:
  display_name: itables
  language: python
  name: itables
---

# Downsampling

When an interactive table is displayed by `itables`, the table data is embedded in the notebook output. As we don't want your notebook to become super heavy just because you displayed a large table, we have a downsampling mechanism in place.

When the data in a table is larger than `maxBytes`, which is equal to 64KB by default, `itables` will display only a subset of the table - one that fits into `maxBytes`, and display a warning that points to the `itables` documentation.

If you wish, you can increase the value of `maxBytes` or even deactivate the limit (with `maxBytes=0`). Similarly you can set a limit on the number of rows (`maxRows`, defaults to 0) or columns (`maxColumns`, defaults to `pd.get_option('display.max_columns')`).

```{code-cell}
from itables import init_notebook_mode, show

init_notebook_mode(all_interactive=True)
```

```{code-cell}
from itables.sample_dfs import get_indicators
import itables.options as opt

opt.lengthMenu = [2, 5, 10, 20, 50, 100, 200, 500]
opt.maxBytes = 10000

df = get_indicators()
df.values.nbytes
```

```{code-cell}
:tags: [full-width]

df
```

To show the table in full, we can modify the value of `maxBytes` either locally:

```{code-cell}
:tags: [full-width]

show(df, maxBytes=0)
```

or globally:

```{code-cell}
:tags: [full-width]

opt.maxBytes = 2**20
df
```
