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

# Pandas Style

Starting with `itable>=1.6.0`, ITables provides support for the Pandas Styler objects.

For instance, the `Styler` object below was constructed following the
[Pandas Style guide](https://pandas.pydata.org/docs/user_guide/style.html),
and is rendered as an interactive datatable when the `all_interactive` mode is
activated:

```{code-cell}
from itables import init_notebook_mode
from itables.sample_dfs import get_pandas_styler

init_notebook_mode(all_interactive=True)
```

```{code-cell}
get_pandas_styler()
```

```{note}
Unlike Pandas or Polar DataFrames, `Styler` objects are rendered directly using the object's
`.to_html` method. For this reason the rendering might slightly differ from the rendering
of DataFrames. Similarly, the downsampling is not available for these objects.
```
