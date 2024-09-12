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

# Jupyter Widget

ITables is also available as a [Jupyter Widget](https://ipywidgets.readthedocs.io).

Make sure you install [AnyWidget](https://github.com/manzt/anywidget), the framework that we use to provide our widget:
```bash
pip install anywidget
```

Then, create a table widget with `ITable` from `itables.widget`:

```{code-cell}
from itables.sample_dfs import get_countries
from itables.widget import ITable

df = get_countries(html=False)
dt = ITable(df)
```

```{code-cell}
dt
```

The `ITable` class accepts the same arguments as the `show` method. It comes with a few limitations - the same as for the [streamlit component](streamlit.md#limitations), e.g. you can't pass JavaScript callback.
