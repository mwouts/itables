# Shiny

The HTML representation returned by `to_html_aggrid` can be inserted
directly in [Shiny](https://shiny.posit.co/py/) applications with
`ui.HTML`, like in this example:

```{include} ../../../apps/shiny/pyaggrid/app.py
:code: python
```

```{tip}
If you need to react to the selected rows, use the `ITable` widget of
[`pydatatables`](../../apps/shiny.html) instead.
```
