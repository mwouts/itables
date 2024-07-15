---
jupytext:
  formats: md:myst
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

# Dark Themes

When a notebook or application is rendered using a dark theme, DataTable requires that a `dark`
class be added to the HTML document. This can be done with the following Javascript snippet:
```javascript
document.documentElement.classList.add('dark');
```

When ITables is used in a notebook, this is handled by
`init_notebook_mode` which displays the [`init_datatables.html`](https://github.com/mwouts/itables/blob/main/src/itables/html/init_datatables.html) snippet.

Please open a PR if you see how to further improve the
support of light vs dark themes, and e.g. set the `dark`
class dynamically when the theme is changed.
