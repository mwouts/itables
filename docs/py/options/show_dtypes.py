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
# # Show DTypes
#
# By default, the columns dtypes are shown only for Polars dataframes. If you prefer, you can change the value of `show_dtypes` to either `True` or `False` to always or never show the index (the default value being `"auto"`).

# %%
import itables

itables.init_notebook_mode()

# %% [markdown]
# You can change this behavior globally with e.g.
# ```python
# itables.options.show_dtypes = True
# ```
#
# or locally by passing an argument `show_dtypes` to the `show` function:

# %%
itables.show(itables.sample_dfs.get_countries(), show_dtypes=True)
