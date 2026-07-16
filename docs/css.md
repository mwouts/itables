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
# pyright: reportUnknownVariableType=false
```

# CSS

You can use CSS to alter how tables are rendered.

The recommended way to do this is to pass your CSS to `itables.options.css`
(or to the `css` argument of `show`). This CSS is embedded in the HTML
output of every table, so it is always guaranteed to be applied - unlike a
standalone `display(HTML(f"<style>{css}</style>"))` cell, which some
notebook front-ends (e.g. VS Code) may not render until that specific cell
output is scrolled into view, see [issue #572](https://github.com/mwouts/itables/issues/572).

For instance, we change the
[font size](https://developer.mozilla.org/en-US/docs/Web/CSS/font-size)
for all the tables in the document with this code:

```{code-cell} ipython3
import itables

itables.options.css = """
.dt-container {
  font-size: small;
}
"""

itables.init_notebook_mode()

df = itables.sample_dfs.get_countries()

itables.show(df)
```

This is helpful for instance in the context of
[Quarto presentations](apps/quarto.md).

With this CSS override, we change _every datatable_ table header
in the notebook to bold/italic.

```{code-cell} ipython3
itables.options.css = """
.dataTable th {
    font-weight: bolder;
    font-style: italic;
}
"""

itables.show(df)
```

You might also want to alter the style of specific tables only.
To do this, either pass CSS to the `css` argument of `show` (rather than to
`itables.options.css`), or add a new class to the target tables and target
that class in your CSS, as in the example below:

```{code-cell} ipython3
class_specific_css = ".table_with_monospace_font { font-family: courier, monospace }"

itables.show(
    df,
    css=class_specific_css,
    classes="display nowrap table_with_monospace_font",
)
```

```{tip}
You can also inject CSS with `display(HTML(f"<style>{css}</style>"))`. This
still works, but the CSS only takes effect once that specific cell's output
has been rendered by the notebook front-end - in VS Code, an output that is
scrolled out of view may not be rendered until you scroll back to it, so the
`itables.options.css`/`css=` approach above is more reliable.
```

```{code-cell} ipython3
:tags: [remove-cell]

itables.options.css = ""
```
