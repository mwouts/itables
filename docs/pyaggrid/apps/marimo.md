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

# Marimo

```{warning}
The `init_notebook_mode` and the `show` functions do not work in Marimo. This is because they both use `IPython.display` to display the HTML representation of the table, which is not a good fit for Marimo.
```

In Marimo, use `to_html_aggrid` in combination with `mo.iframe`:

```python
import marimo as mo

from itables_core.sample_dfs import get_dict_of_test_dfs
from pyaggrid import to_html_aggrid

df = get_dict_of_test_dfs()["int_float_str"]

html = to_html_aggrid(df)
mo.iframe(html)
```

A sample Marimo application is available at
[`apps/marimo/pyaggrid.py`](https://github.com/mwouts/itables/tree/main/apps/marimo/pyaggrid.py).
