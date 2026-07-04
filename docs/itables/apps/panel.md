# Panel

## Using `ITable` in Panel

The recommended way to use ITables in a [Panel](https://panel.holoviz.org)
application is with the [ITable Widget](widget.md).

Panel can render ipywidgets like `ITable` through its
`ipywidgets` extension, which requires the
`ipywidgets_bokeh` and `ipykernel` packages:

```python
import panel as pn

from itables.widget import ITable

pn.extension("ipywidgets")

# Note: df is an optional argument
table = ITable(caption="A table rendered with ITable", select=True)
```

The widget can be inserted in any Panel layout or template, e.g.

```python
pn.Column(pn.panel(table, sizing_mode="stretch_width")).servable()
```

## Updating the widget

Rather than re-creating the widget each time the data changes, you should
call the `.update` method of the widget object. Use `param.watch` to trigger
the update when another widget changes, e.g. when the active tab changes:

```python
names = list(dfs.keys())

table_tabs = pn.Tabs(
    *[(name, pn.pane.Str("")) for name in names],
    active=names.index("int_float_str"),
    dynamic=True,
)


def on_tab_change(event) -> None:
    df = dfs[names[event.new]]
    table.update(df, selected_rows=list(range(0, len(df), 3)))


table_tabs.param.watch(on_tab_change, "active")
```

## Accessing the `selected_rows` attribute

The `selected_rows` attribute of the `ITable` widget is a
traitlets trait, so you can observe it to react to selection changes:

```python
selected_rows = pn.pane.Markdown()


def on_selected_rows_change(change) -> None:
    selected_rows.object = f"Selected rows: `{change['new']}`"


table.observe(on_selected_rows_change, names="selected_rows")
```

## An example application

The ITables [repository](https://github.com/mwouts/itables/tree/main/apps/panel) contains a simple
example of a Panel application that uses the `ITable` widget. Run it locally with

```bash
pixi run -e panel-app panel serve apps/panel/itables_app.py
```

A live version is hosted on [Hugging Face Spaces](https://huggingface.co/spaces/mwouts/itables):

```{div} full-width
<iframe src="https://mwouts-itables.hf.space"
style="height: 800px; width: 100%;"></iframe>
```

## Hosting a Panel application

Panel applications can be hosted for free on
[Hugging Face Spaces](https://panel.holoviz.org/how_to/deployment/huggingface.html)
(a Panel template is available there) or on [PyCafe](https://py.cafe/docs/apps/panel).
Hugging Face Spaces runs `panel serve` in a Docker container, so the `ITable`
widget works there just like locally. See the
[Panel deployment guide](https://panel.holoviz.org/how_to/deployment/index.html)
for more options.
