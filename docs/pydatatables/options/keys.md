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

# Keys

With the [KeyTable](https://datatables.net/extensions/keytable/) extension you can navigate in a table using the arrow keys:

```{code-cell} ipython3
:tags: [full-width]

import itables

itables.init_notebook_mode()

itables.show(
    itables.sample_dfs.get_countries(),
    keys=True,
)
```

```{tip}
You can activate this option for all your tables with

~~~python
itables.options.keys = True
~~~
```

```{warning}
The KeyTable extension works in Jupyter Book (try it here in the documentation) but not in JupyterLab.
```
