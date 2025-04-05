---
jupytext:
  formats: md:myst
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
