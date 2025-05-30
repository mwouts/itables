---
jupytext:
  formats: docs///md:myst,docs/py///py:percent
  notebook_metadata_filter: -jupytext.text_representation.jupytext_version
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
kernelspec:
  display_name: itables
  language: python
  name: itables
---

# Pandas dataframes

In this notebook we make sure that our test dataframes are displayed nicely with the default `itables` settings.

```{code-cell} ipython3
import itables

dict_of_test_dfs = itables.sample_dfs.get_dict_of_test_dfs()
itables.init_notebook_mode()
```

## empty

```{code-cell} ipython3
itables.show(dict_of_test_dfs["empty"])
```

## No rows

```{code-cell} ipython3
itables.show(dict_of_test_dfs["no_rows"])
```

## No rows one column

```{code-cell} ipython3
itables.show(dict_of_test_dfs["no_rows_one_column"])
```

## No columns

```{code-cell} ipython3
itables.show(dict_of_test_dfs["no_columns"])
```

## No columns one row

```{code-cell} ipython3
itables.show(dict_of_test_dfs["no_columns_one_row"])
```

## bool

```{code-cell} ipython3
itables.show(dict_of_test_dfs["bool"])
```

## Nullable boolean

```{code-cell} ipython3
itables.show(dict_of_test_dfs["nullable_boolean"])
```

## int

```{code-cell} ipython3
itables.show(dict_of_test_dfs["int"])
```

## Nullable integer

```{code-cell} ipython3
itables.show(dict_of_test_dfs["nullable_int"])
```

## float

```{code-cell} ipython3
itables.show(dict_of_test_dfs["float"])
```

## str

```{code-cell} ipython3
itables.show(dict_of_test_dfs["str"])
```

## time

```{code-cell} ipython3
itables.show(dict_of_test_dfs["time"])
```

## object

```{code-cell} ipython3
itables.show(dict_of_test_dfs["object"])
```

## ordered_categories

```{code-cell} ipython3
itables.show(dict_of_test_dfs["ordered_categories"])
```

## ordered_categories_in_multiindex

```{code-cell} ipython3
itables.show(dict_of_test_dfs["ordered_categories_in_multiindex"])
```

## multiindex

```{code-cell} ipython3
itables.show(dict_of_test_dfs["multiindex"])
```

## countries

```{code-cell} ipython3
:tags: [full-width]

itables.show(dict_of_test_dfs["countries"])
```

## capital

```{code-cell} ipython3
itables.show(dict_of_test_dfs["capital"])
```

## complex_index

```{code-cell} ipython3
:tags: [full-width]

itables.show(dict_of_test_dfs["complex_index"])
```

## int_float_str

```{code-cell} ipython3
itables.show(dict_of_test_dfs["int_float_str"])
```

## wide

```{code-cell} ipython3
:tags: [full-width]

itables.show(dict_of_test_dfs["wide"], maxBytes=100000, maxColumns=100, scrollX=True)
```

## long_column_names

```{code-cell} ipython3
:tags: [full-width]

itables.show(dict_of_test_dfs["long_column_names"], scrollX=True)
```

## duplicated_columns

```{code-cell} ipython3
itables.show(dict_of_test_dfs["duplicated_columns"])
```

## named_column_index

```{code-cell} ipython3
itables.show(dict_of_test_dfs["named_column_index"])
```

## big_integers

```{code-cell} ipython3
itables.show(dict_of_test_dfs["big_integers"])
```
