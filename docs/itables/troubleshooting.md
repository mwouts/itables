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
# pyright: reportDuplicateImport=false
```

# Troubleshooting

## Loading takes forever?

```{code-cell} ipython3
:tags: [hide-input]

import pandas as pd

import itables

df = pd.DataFrame()

itables.show(df, connected=False)
```

If a table says "Loading..." forever, then maybe
- You forgot to run `init_notebook_mode` (like in the example above), or you deleted that cell or its output
- Or you ran `init_notebook_mode(connected=True)` but you are not connected to the internet?

```{tip}
If you change the value of the `connected` argument in
the `init_notebook_mode` cell, you need to re-execute all the cells
that display interactive tables.
```

## Trust your notebook

It could also be because your notebook is not _trusted_. This happens when you
have not run the notebook in full yourself (e.g. the notebook was sent to you with outputs,
or the notebook was created by a tool like `papermill`). In that case, JavaScript
code cannot run (and the interactive tables won't display)
until you tell Jupyter that you trust the notebook content
(run "Trust Notebook" in View / Activate Command Palette).

## Check ITables' version

If the above does not help, please check out the [ChangeLog](changelog.md)
and decide whether you should upgrade `itables`. You can tell the version
of ITables that you are using by looking at the loading message (from ITables v2.0.1 on)
or by running this code snippet:

```{code-cell} ipython3
import itables

itables.__version__
```
