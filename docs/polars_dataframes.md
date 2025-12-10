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

# Polars dataframes

In this notebook we make sure that our test [Polars](https://www.pola.rs/)
dataframes are displayed nicely with the default `itables` settings.

```{code-cell} ipython3
import itables

dict_of_test_dfs = itables.sample_polars_dfs.get_dict_of_test_dfs()
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

## ordered_categories

```{code-cell} ipython3
itables.show(dict_of_test_dfs["ordered_categories"])
```

## countries

```{code-cell} ipython3
:tags: [full-width]

itables.show(dict_of_test_dfs["countries"])
```

## int_float_str

```{code-cell} ipython3
itables.show(dict_of_test_dfs["int_float_str"])
```

## wide

```{code-cell} ipython3
:tags: [full-width]

itables.show(dict_of_test_dfs["wide"], maxBytes=100000, maxColumns=100)
```

## long_column_names

```{code-cell} ipython3
:tags: [full-width]

itables.show(dict_of_test_dfs["long_column_names"])
```

## big_integers

```{code-cell} ipython3
itables.show(dict_of_test_dfs["big_integers"])
```
