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

# Using Pandas Style

Starting with `itables>=1.6.0`, ITables provides support for
[Pandas Style](https://pandas.pydata.org/docs/user_guide/style.html).

```{note}
Unlike Pandas or Polar DataFrames, `Styler` objects are rendered directly using their
`to_html` method, rather than passing the underlying table data to the DataTables
library.

Because of this, the rendering of the table might differ slightly from the rendering of the
corresponding DataFrame. In particular,
- The downsampling is not available - please pay attention to the size of the table being rendered
- Sorting of numbers will not work if the column contains NaNs.
```

```{warning}
Pandas Style objects can't be used with the [Streamlit extension](streamlit.md) for ITables.
```

```{code-cell}
import numpy as np
import pandas as pd

from itables import init_notebook_mode

init_notebook_mode(all_interactive=True)
```

```{code-cell}
:tags: [remove-input]

import itables.options as opt

opt.lengthMenu = [5, 10, 20, 50, 100, 200, 500]
```

This is the DataFrame that we are going to style:

```{code-cell}
x = np.linspace(0, np.pi, 21)
df = pd.DataFrame({"sin": np.sin(x), "cos": np.cos(x)}, index=pd.Index(x, name="alpha"))

df
```

## Color

From now on we will display `df.style`
(a Pandas `Styler` object) rather than our DataFrame `df`.

Let's start with a background gradient:

```{code-cell}
s = df.style
s.background_gradient(axis=None, cmap="YlOrRd")
```

## Format

We can also choose how the data is formatted:

```{code-cell}
s.format("{:.3f}").format_index("{:.3f}")
```

## Caption

```{code-cell}
s.set_caption("A Pandas Styler object with background colors").set_table_styles(
    [{"selector": "caption", "props": "caption-side: bottom; font-size:1em;"}]
)
```

## Tooltips

```{code-cell}
ttips = pd.DataFrame(
    {
        "sin": ["The sinus of {:.6f} is {:.6f}".format(t, np.sin(t)) for t in x],
        "cos": ["The cosinus of {:.6f} is {:.6f}".format(t, np.cos(t)) for t in x],
    },
    index=df.index,
)
s.set_tooltips(ttips).set_caption("With tooltips")
```
