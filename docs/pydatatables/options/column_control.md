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

# Column Control

The [`columnControl`](https://datatables.net/extensions/columncontrol/config) option lets you add column specific controls.

The examples should give you a quick sense of how to use `columnControl`. You are invited to consult the datatables documentation for many more column control [examples](https://datatables.net/extensions/columncontrol/examples/) - see also Allan's [post](https://datatables.net/blog/2025/columncontrol) in which the extension was introduced.

```{code-cell} ipython3
import itables

itables.init_notebook_mode()

df = itables.sample_dfs.get_countries()
```

## Getting started

The `columnControl` option can take as value the list of controls that should be added to the table columns.

```{code-cell} ipython3
:tags: [full-width]

itables.show(
    df,
    columnControl=["order", "colVisDropdown", "searchDropdown"],
    ordering={"indicators": False, "handler": False},
)
```

```{tip}
When an ordering option is provided through the `columnControl` option,
you probably want to deactivate the default ordering icons - that's the purpose of
`ordering={"indicators": False, "handler": False}` used in the example above.
```

## Drop-downs

Nested lists are mapped to dropdowns:

```{code-cell} ipython3
:tags: [full-width]

itables.show(
    df,
    columnControl=["order", ["orderAsc", "orderDesc", "search"]],
    ordering={"indicators": False, "handler": False},
)
```

## Controls and table footers

The column controls can also be added to a table footer:

```{code-cell} ipython3
:tags: [full-width]

itables.show(
    df,
    columnControl=[
        {"target": 0, "content": ["order"]},
        {"target": "tfoot", "content": ["search"]},
    ],
    ordering={"indicators": False, "handler": False},
)
```

As usual, you can make this the default by either setting `itables.options.columnControl` in your notebook or application, or by adding this to your `itables.toml` [configuration file](../configuration.md):
```
[[columnControl]]
target = 0
content = ["order"]
[[columnControl]]
target = "tfoot"
content = ["search"]

[ordering]
indicators = false
handler = false
```
