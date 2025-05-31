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

# pyright: reportUnknownVariableType=false
```

# HTML export

To get the HTML representation of a Pandas DataFrame `df` as an interactive [DataTable](https://datatables.net/), you can use `to_html_datatable` as below:

```{code-cell} ipython3
from IPython.display import HTML, display

import itables

df = itables.sample_dfs.get_countries(html=False)
html = itables.to_html_datatable(df.head(3), display_logo_when_loading=False)
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

~~~{admonition} The `connected` argument
:class: tip
The `to_html_datatable` function has a `connected` argument which defaults to what you set in `init_notebook_mode` (it's `True` if you didn't call it).

- With `connected=True` you get an autonomous HTML fragment that loads `dt_for_itables` from the Internet
- With `connected=False`, the HTML snippet works only after you add the output of `generate_init_offline_itables_html()` to your HTML document
~~~
