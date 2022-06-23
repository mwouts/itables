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

# DataTables Plugins

The [DataTables](https://datatables.net/) comes with many plugins. In the below we document how to use a few of them.

## Search highlighting

The search highlight with mark.js is documented in this
[datatables blog post](https://datatables.net/blog/2017-01-19).

### Search highlighting in the connected mode

We start with the connected mode:

```{code-cell}
from itables import init_notebook_mode, show

# init_notebook_mode(connected=True)
```

In that mode, you just need to pass the plugins URLs to the `show` function:

```{code-cell}
from itables.sample_dfs import get_alpha_numeric_df

df = get_alpha_numeric_df()
show(
    df,
    # As documented in the blog post
    mark=True,
    # The URLs for the plugins, again from the blog post
    dt_plugins=[
        "https://cdn.jsdelivr.net/g/mark.js(jquery.mark.min.js)",
        "https://cdn.datatables.net/plug-ins/1.12.1/features/mark.js/datatables.mark.js",
    ],
    # Set an initial input in the search field
    search={"search": "e"},
)
```

You can also set a default value for `dt_plugins` with e.g.

```{code-cell}
import itables.options as opt

opt.dt_plugins = [
    "https://cdn.jsdelivr.net/g/mark.js(jquery.mark.min.js)",
    "https://cdn.datatables.net/plug-ins/1.12.1/features/mark.js/datatables.mark.js",
]
```

### Search highlighting in the offline mode

In the offline mode we assume that you have downloaded the libraries on disk with e.g.:

```{code-cell}
:tags: [hide-input]

import requests
from pathlib import Path

dt_plugins_dir = Path.home() / ".itables" / "offline_dt_plugins"
dt_plugins_dir.mkdir(exist_ok=True)

for filename, url in [
    ("mark.js", "https://cdn.jsdelivr.net/g/mark.js(jquery.mark.min.js)"),
    (
        "datatables.mark.js",
        "https://cdn.datatables.net/plug-ins/1.12.1/features/mark.js/datatables.mark.js",
    ),
]:
    r = requests.get(url)
    (dt_plugins_dir / filename).write_bytes(r.content)

# To avoid a warning when we call show in the offline mode
opt.dt_plugins = []
```

The offline plugins are loaded by `init_notebook_mode`

```{code-cell}
init_notebook_mode(
    connected=False, offline_dt_plugins=[plugin for plugin in dt_plugins_dir.iterdir()]
)
```

```{code-cell}
show(
    df,
    # As documented in the blog post
    mark=True,
    # Set an initial input in the search field
    search={"search": "e"},
)
```

```{code-cell}

```
