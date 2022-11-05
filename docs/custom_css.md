---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.13.8
kernelspec:
  display_name: itables
  language: python
  name: itables
---

## Custom CSS

You can change the CSS used to render the tables
by either passing a custom CSS to the `show` function, or by
changing `opt.css`. Note that the CSS must be the same for all the tables
in a given notebook.

```{code-cell}
from itables import init_notebook_mode, show
from itables.sample_dfs import get_countries
import itables.options as opt


opt.css = """
.itables table td { font-style: italic; }
.itables table th { font-style: oblique; }
"""

init_notebook_mode(all_interactive=True)
```

```{code-cell}
get_countries()
```
