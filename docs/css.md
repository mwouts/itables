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
```

# CSS

You can use CSS to alter how tables are rendered.

For instance, we change the
[font size](https://developer.mozilla.org/en-US/docs/Web/CSS/font-size)
for all the tables in the document with this code:

```{code-cell} ipython3
from IPython.display import HTML, display

css = """
.dt-container {
  font-size: small;
}
"""
display(HTML(f"<style>{css}</style>" ""))
```

This is helpful for instance in the context of
[Quarto presentations](apps/quarto.md).

With this over CSS, we change _every datatable_ table header
in the notebook to bold/italic.

```{code-cell} ipython3
css = """
.dataTable th {
    font-weight: bolder;
    font-style: italic;
}
"""
display(HTML(f"<style>{css}</style>" ""))
```

You might also want to alter the style of specific tables only.
To do this, add a new class to the target tables, as
in the example below:

```{code-cell} ipython3
class_specific_css = ".table_with_monospace_font { font-family: courier, monospace }"
display(HTML(f"<style>{class_specific_css}</style>" ""))
```

```{code-cell} ipython3
:tags: [full-width]

import itables

itables.init_notebook_mode()

df = itables.sample_dfs.get_countries(html=False)

itables.show(df, classes="display nowrap table_with_monospace_font")
```
