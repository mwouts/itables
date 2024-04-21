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

# Troubleshooting

If the table just says "Loading...", then maybe
- You loaded a notebook that is not trusted (run "Trust Notebook" in View / Activate Command Palette)
- You forgot to run `init_notebook_mode`, or you deleted that cell or its output
- Or you ran `init_notebook_mode(connected=True)` but you are not connected to the internet?

Please note that if you change the value of the `connected` argument in
the `init_notebook_mode` cell, you will need to re-execute all the cells
that display interactive tables.

If the above does not help, please check out the [ChangeLog](changelog.md)
and decide whether you should upgrade `itables`.

```{code-cell}
import pandas as pd

from itables import show

df = pd.DataFrame()
tags = (
    '<caption style="caption-side: bottom">A table that does not load, due '
    "to <code>init_notebook_mode</code><br>not being called in this document</caption>"
)

show(df, connected=False, tags=tags)
```
