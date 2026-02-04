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

# Classes

Select how your table looks like with the `classes` argument of the `show` function, or by changing `itables.options.classes`.

The default value for `classes` is `"display nowrap compact"` (`"compact"` was added in ITables v2.7).

Remove `"compact"` if you want a less dense table:

```{code-cell} ipython3
:tags: [full-width]

import pandas as pd

import itables

itables.init_notebook_mode()

df = itables.sample_dfs.get_countries()

itables.show(df, classes="display nowrap")
```

Remove `"nowrap"` if you want the cell content to be wrapped:

```{code-cell} ipython3
:tags: [full-width]

itables.show(
    pd.DataFrame({"text": ["This is a " + "very " * 60 + "long text"]}),
    classes="display compact",
)
```

[More options](https://datatables.net/manual/styling/classes#Table-classes) like `"cell-border"` are available:

```{code-cell} ipython3
:tags: [full-width]

itables.show(df, classes="display nowrap compact cell-border")
```

```{tip}
You can change the default for all your notebooks and apps by creating an `itables.toml` [configuration file](../configuration.md) in the current or a parent directory, with e.g. this content:
~~~
classes = ["display", "nowrap"]
~~~
```
