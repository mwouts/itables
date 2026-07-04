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
# # Show Index
#
# By default, the index of a Series/DataFrame is shown only when not trivial, i.e. when it has a name, or when it differs from a range index. If you prefer, you can change the value of `showIndex` to either `True` or `False` to always or never show the index (the default value being `"auto"`).

# %%
import pandas as pd

import itables

itables.init_notebook_mode()

# %% [markdown]
# You can change this behavior globally with e.g.
# ```python
# itables.options.showIndex = True
# ```
#
# or locally by passing an argument `showIndex` to the `show` function:

# %%
df_with_range_index = pd.DataFrame({"letter": list("abcd")})
itables.show(df_with_range_index, showIndex=True)
