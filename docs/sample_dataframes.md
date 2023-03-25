---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.14.5
kernelspec:
  display_name: itables
  language: python
  name: itables
---

# Sample dataframes

In this notebook we make sure that our test dataframes are displayed nicely with the default `itables` settings.

```{code-cell}
from itables import init_notebook_mode, show
from itables.sample_dfs import get_dict_of_test_dfs

dict_of_test_dfs = get_dict_of_test_dfs()
init_notebook_mode(all_interactive=True)
```

## empty

```{code-cell}
show(dict_of_test_dfs["empty"])
```

## bool

```{code-cell}
show(dict_of_test_dfs["bool"])
```

## Nullable boolean

```{code-cell}
show(dict_of_test_dfs["nullable_boolean"])
```

## int

```{code-cell}
show(dict_of_test_dfs["int"])
```

## Nullable integer

```{code-cell}
show(dict_of_test_dfs["nullable_int"])
```

## float

```{code-cell}
show(dict_of_test_dfs["float"])
```

## str

```{code-cell}
show(dict_of_test_dfs["str"])
```

## time

```{code-cell}
show(dict_of_test_dfs["time"])
```

## object

```{code-cell}
show(dict_of_test_dfs["object"])
```

## ordered_categories

```{code-cell}
show(dict_of_test_dfs["ordered_categories"])
```

## ordered_categories_in_multiindex

```{code-cell}
show(dict_of_test_dfs["ordered_categories_in_multiindex"])
```

## multiindex

```{code-cell}
show(dict_of_test_dfs["multiindex"])
```

## countries

```{code-cell}
:tags: [full-width]

show(dict_of_test_dfs["countries"])
```

## capital

```{code-cell}
show(dict_of_test_dfs["capital"])
```

## complex_index

```{code-cell}
:tags: [full-width]

show(dict_of_test_dfs["complex_index"])
```

## int_float_str

```{code-cell}
show(dict_of_test_dfs["int_float_str"])
```

## wide

```{code-cell}
:tags: [full-width]

show(dict_of_test_dfs["wide"], maxBytes=100000, maxColumns=100, scrollX=True)
```

## long_column_names

```{code-cell}
:tags: [full-width]

show(dict_of_test_dfs["long_column_names"], scrollX=True)
```

## duplicated_columns

```{code-cell}
show(dict_of_test_dfs["duplicated_columns"])
```

## named_column_index

```{code-cell}
show(dict_of_test_dfs["named_column_index"])
```

## big_integers

```{code-cell}
import itables.options as opt

opt.warn_on_int_to_str_conversion = False

show(dict_of_test_dfs["big_integers"])
```
