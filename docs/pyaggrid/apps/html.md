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

# ruff: noqa: E402
# pyright: reportUnusedExpression=false
```

# HTML export

To get the HTML representation of a Pandas DataFrame `df` as an interactive [AG Grid](https://www.ag-grid.com/) table, you can use `to_html_aggrid` as below:

import itables_core.sample_dfs
import pyaggrid

```{code-cell} ipython3
from IPython.display import HTML, display

df = itables_core.sample_dfs.get_countries()
html = pyaggrid.to_html_aggrid(df.head(3))
```

You can then save the `html` variable to a text file (note: if you're writing an HTML application, you could consider using [Shiny](shiny.md) or [Streamlit](streamlit.md) instead), or print it:

```{code-cell} ipython3
:tags: [scroll-output]

print(html)
```

or display it, like `show` does:

```{code-cell} ipython3
display(HTML(html))
```

~~~{admonition} An internet connection is required
:class: tip
The HTML snippet returned by `to_html_aggrid` loads AG Grid Community
from the URL set in `pyaggrid.options.ag_grid_url` (jsDelivr by default),
so an internet connection is required when the table is displayed.
~~~
