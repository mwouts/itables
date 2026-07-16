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

```{code-cell} ipython3
:tags: [remove-cell]

# pyright: reportUnusedExpression=false
```

# Static preview - Pandas dataframes

`itables.to_html_static_preview()` returns the plain HTML table that
`to_html_datatable()` shows by default, ahead of the interactive table -
see [Static preview](static_preview.md) for why, and when, this is shown
instead. This page shows it for each of our test
Pandas dataframes; see [Pandas dataframes](../pandas_dataframes.md) for the
same dataframes rendered as interactive tables.

```{code-cell} ipython3
from IPython.display import HTML, display

import itables

dict_of_test_dfs = itables.sample_pandas_dfs.get_dict_of_test_dfs()
```

## empty

```{code-cell} ipython3
display(HTML(itables.to_html_static_preview(dict_of_test_dfs["empty"])))
```

## No rows

```{code-cell} ipython3
display(HTML(itables.to_html_static_preview(dict_of_test_dfs["no_rows"])))
```

## No columns

```{code-cell} ipython3
display(HTML(itables.to_html_static_preview(dict_of_test_dfs["no_columns"])))
```

## No rows one column

```{code-cell} ipython3
display(HTML(itables.to_html_static_preview(dict_of_test_dfs["no_rows_one_column"])))
```

## No columns one row

```{code-cell} ipython3
display(HTML(itables.to_html_static_preview(dict_of_test_dfs["no_columns_one_row"])))
```

## bool

```{code-cell} ipython3
display(HTML(itables.to_html_static_preview(dict_of_test_dfs["bool"])))
```

## Nullable boolean

```{code-cell} ipython3
display(HTML(itables.to_html_static_preview(dict_of_test_dfs["nullable_boolean"])))
```

## int

```{code-cell} ipython3
display(HTML(itables.to_html_static_preview(dict_of_test_dfs["int"])))
```

## Nullable integer

```{code-cell} ipython3
display(HTML(itables.to_html_static_preview(dict_of_test_dfs["nullable_int"])))
```

## float

```{code-cell} ipython3
display(HTML(itables.to_html_static_preview(dict_of_test_dfs["float"])))
```

## float_types

```{code-cell} ipython3
display(HTML(itables.to_html_static_preview(dict_of_test_dfs["float_types"])))
```

## str

```{code-cell} ipython3
display(HTML(itables.to_html_static_preview(dict_of_test_dfs["str"])))
```

## time

```{code-cell} ipython3
display(HTML(itables.to_html_static_preview(dict_of_test_dfs["time"])))
```

## date_range

```{code-cell} ipython3
display(HTML(itables.to_html_static_preview(dict_of_test_dfs["date_range"])))
```

## ordered_categories

```{code-cell} ipython3
display(HTML(itables.to_html_static_preview(dict_of_test_dfs["ordered_categories"])))
```

## ordered_categories_in_multiindex

```{code-cell} ipython3
display(
    HTML(
        itables.to_html_static_preview(
            dict_of_test_dfs["ordered_categories_in_multiindex"]
        )
    )
)
```

## object

```{code-cell} ipython3
display(HTML(itables.to_html_static_preview(dict_of_test_dfs["object"])))
```

## multiindex

```{code-cell} ipython3
display(HTML(itables.to_html_static_preview(dict_of_test_dfs["multiindex"])))
```

## countries

```{code-cell} ipython3
:tags: [full-width]

display(HTML(itables.to_html_static_preview(dict_of_test_dfs["countries"])))
```

## capital

```{code-cell} ipython3
display(HTML(itables.to_html_static_preview(dict_of_test_dfs["capital"])))
```

## complex_index

```{code-cell} ipython3
:tags: [full-width]

display(HTML(itables.to_html_static_preview(dict_of_test_dfs["complex_index"])))
```

## int_float_str

```{code-cell} ipython3
display(HTML(itables.to_html_static_preview(dict_of_test_dfs["int_float_str"])))
```

## wide

```{code-cell} ipython3
:tags: [full-width]

display(HTML(itables.to_html_static_preview(dict_of_test_dfs["wide"])))
```

## long_column_names

```{code-cell} ipython3
:tags: [full-width]

display(HTML(itables.to_html_static_preview(dict_of_test_dfs["long_column_names"])))
```

## sorted_index

```{code-cell} ipython3
display(HTML(itables.to_html_static_preview(dict_of_test_dfs["sorted_index"])))
```

## reverse_sorted_index

```{code-cell} ipython3
display(HTML(itables.to_html_static_preview(dict_of_test_dfs["reverse_sorted_index"])))
```

## sorted_multiindex

```{code-cell} ipython3
display(HTML(itables.to_html_static_preview(dict_of_test_dfs["sorted_multiindex"])))
```

## unsorted_index

```{code-cell} ipython3
display(HTML(itables.to_html_static_preview(dict_of_test_dfs["unsorted_index"])))
```

## duplicated_columns

```{code-cell} ipython3
display(HTML(itables.to_html_static_preview(dict_of_test_dfs["duplicated_columns"])))
```

## named_column_index

```{code-cell} ipython3
display(HTML(itables.to_html_static_preview(dict_of_test_dfs["named_column_index"])))
```

## big_integers

```{code-cell} ipython3
display(HTML(itables.to_html_static_preview(dict_of_test_dfs["big_integers"])))
```
