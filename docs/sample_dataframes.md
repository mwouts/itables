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

```{code-cell} ipython3
from itables import init_notebook_mode, show
from itables.sample_dfs import get_dict_of_test_dfs, get_dict_of_test_series
from IPython.display import display, Markdown

dict_of_test_dfs = get_dict_of_test_dfs()
init_notebook_mode(all_interactive=True)
```

````{code-cell} ipython3
"""
# We first tried to generate all the examples with this code
# but that is not supported atm by jp, see
# https://github.com/executablebooks/jupyter-book/issues/1610
for df_name, df in get_dict_of_test_dfs().items():
    display(Markdown(f"## {df_name}"))
    display(show(df, maxBytes=1e5, maxColumns=100))
"""

"""
# So instead we generated the content of this notebook with
cells = []
for df_name in dict_of_test_dfs:
    cells.append(f"## {df_name}")
    cells.append(f'''

```{{code-cell}}
show(dict_of_test_dfs["{df_name}"])
```
''')

print('\n'.join(cells))
""";
````

## empty

```{code-cell} ipython3
show(dict_of_test_dfs["empty"])
```

## int

```{code-cell} ipython3
show(dict_of_test_dfs["int"])
```

## float

```{code-cell} ipython3
show(dict_of_test_dfs["float"])
```

## str

```{code-cell} ipython3
show(dict_of_test_dfs["str"])
```

## time

```{code-cell} ipython3
show(dict_of_test_dfs["time"])
```

## object

```{code-cell} ipython3
show(dict_of_test_dfs["object"])
```

## multiindex

```{code-cell} ipython3
show(dict_of_test_dfs["multiindex"])
```

## countries

```{code-cell} ipython3
show(dict_of_test_dfs["countries"])
```

## capital

```{code-cell} ipython3
show(dict_of_test_dfs["capital"])
```

## complex_index

```{code-cell} ipython3
show(dict_of_test_dfs["complex_index"])
```

## int_float_str

```{code-cell} ipython3
show(dict_of_test_dfs["int_float_str"])
```

## wide

```{code-cell} ipython3
show(dict_of_test_dfs["wide"], maxBytes=100000, maxColumns=100)
```

## long_column_names

```{code-cell} ipython3
show(dict_of_test_dfs["long_column_names"])
```
