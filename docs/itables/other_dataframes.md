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

# Other DataFrames

ITables can render other types of DataFrames than Pandas and Polars
if you have [Narwhals](https://narwhals-dev.github.io/narwhals/) installed.
If you would like to see more examples DataFrames here, please reach
out to us on [GitHub](https://github.com/mwouts/itables).

```{code-cell} ipython3
:tags: [remove-cell]

# pyright: reportMissingTypeStubs=false
# pyright: reportUnknownMemberType=false
```

```{code-cell} ipython3
import modin.pandas as mpd
import pyarrow as pa

import itables
```

## PyArrow

```{code-cell} ipython3
itables.show(pa.table({"A": [1, 2, 3], "B": [4.1, 5.2, 6.3]}))
```

# Modin

```{code-cell} ipython3
itables.show(mpd.DataFrame({"A": [1, 2, 3], "B": [4.1, 5.2, 6.3]}))
```
