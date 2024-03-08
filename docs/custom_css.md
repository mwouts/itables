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

# Custom CSS

## Targeting all tables

You can use CSS to alter how the interactive datatables are rendered.
Use the `.dataTable` class attribute to target all the tables in the notebook, like here:

```{code-cell}
from itables import init_notebook_mode, show
from itables.sample_dfs import get_countries


init_notebook_mode(all_interactive=True)
```

```{code-cell}
from IPython.display import display, HTML


css = """
.dataTable th { font-weight: bolder; }
.dataTable:not(.table_with_monospace_font) tr { font-style: italic; }
"""
display(HTML(f"<style>{css}</style>" ""))
```

```{code-cell}
get_countries()
```

## Targeting specific classes

You might also want to target only specific table like in this example
(note how we add the `table_with_monospace_font` class
to the table using the [`classes`](advanced_parameters.md#classes)
argument of the `show` function):

```{code-cell}
class_specific_css = ".table_with_monospace_font { font-family: courier, monospace }"
display(HTML(f"<style>{class_specific_css}</style>" ""))
```

```{code-cell}
show(get_countries(), classes="display nowrap table_with_monospace_font")
```
