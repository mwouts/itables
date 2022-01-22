---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.11.5
kernelspec:
  display_name: itables
  language: python
  name: itables
---

# Sample dataframes

In this notebook we make sure that our test dataframes are displayed nicely with the default `itables` settings.

```{code-cell}
from itables import init_notebook_mode, show
from itables.sample_dfs import get_dict_of_test_dfs, get_dict_of_test_series
from IPython.display import display, Markdown

init_notebook_mode(all_interactive=True)
```

```{code-cell}
for df_name, df in get_dict_of_test_dfs().items():
    display(Markdown(f"## {df_name}"))
    display(show(df, maxBytes=1e5, maxColumns=100))
```
