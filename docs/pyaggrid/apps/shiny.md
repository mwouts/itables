# Shiny

The HTML representation returned by `to_html_aggrid` can be inserted
directly in [Shiny](https://shiny.posit.co/py/) applications with
`ui.HTML`, like in this example:

```{include} ../../../apps/pyaggrid/shiny/pyaggrid_app/app.py
:code: python
```

## The AgGrid widget in Shiny

If you need to react to the selected rows, use the `AgGrid`
[widget](widget.md) through
[shinywidgets](https://shiny.posit.co/py/docs/jupyter-widgets.html),
like in this example:

```{include} ../../../apps/pyaggrid/shiny/aggrid_widget/app.py
:code: python
```
