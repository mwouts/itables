# ---
# jupyter:
#   jupytext:
#     default_lexer: ipython3
#     formats: docs///md:myst,docs/py///py:percent
#     notebook_metadata_filter: -jupytext.text_representation.jupytext_version
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#   kernelspec:
#     display_name: itables
#     language: python
#     name: itables
# ---

# %% [markdown]
# # Style
#
# The `show` function has a `style` argument that determines the layout for a particular table.
#
# The default value for `style` is `"table-layout:auto;width:auto;margin:auto;caption-side:bottom"`.
# - Without `width:auto`, tables with few columns are stretched to fit the container width.
# - Using `margin:auto` makes non-wide tables centered.

# %% tags=["full-width"]
import pandas as pd

import itables

itables.init_notebook_mode()

df_small = pd.DataFrame({"a": [2, 1]})

# %% [markdown]
# You can set a specific width or position for a table using with the `style` argument of the show function:

# %%
itables.show(df_small, style="table-layout:auto;width:50%;float:right")

# %% [markdown]
# or you can also change it for all tables by changing `itables.options.style`:
#
# ```python
# itables.options.style = "table-layout:auto;width:auto"
# ```
#
# ```{tip}
# The height of a table is governed by either [`lengthMenu`](length_menu.md) or by [`scrollY`](scroll_y.md).
# ```
#
# If you are looking for changing the table content appeareance, see the page on [CSS](../css.md), or the page on [Pandas Style](../pandas_style.md).
