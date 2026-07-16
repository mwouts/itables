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

# pyright: reportUnusedExpression=false
```

# Markdown Preview

## `itables.show()` outside of a notebook

`itables.show()` normally displays an interactive DataTable. But that
requires a notebook (or another IPython-based, HTML-capable frontend) to
render the HTML output in. In a plain Python script, or an interactive
Python session started with just `python` (not `ipython`), there is nowhere
to display HTML at all.

In that case, `itables.show()` falls back to printing a **static preview**:
a Markdown table with just the first rows - 10 by default, or as many as
your `pageLength`/`lengthMenu` options say. This is the same fallback (see
[Static preview](static_preview.md)) that a table gets when it's viewed
somewhere that can't run JavaScript, except that here it's printed as
Markdown - since there is no HTML output at all to embed it in - rather
than shown as a static HTML table.

## `to_markdown_table`

You can also build that Markdown table yourself, with `to_markdown_table`:

```{code-cell} ipython3
import itables

df = itables.sample_dfs.get_countries()
print(itables.to_markdown_table(df))
```

Markdown tables like this one are simple enough for both humans and AI
agents to read directly - e.g. from a script's console output, or from a
notebook's saved JSON when read as a file rather than rendered.
