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
# # Show DataFrame or Series Type
#
# You can display the type of the DataFrame or Series by setting the option
# `show_df_type` to `True`. By default, this option is set to `False`.
#
# The type information appears below the table and shows the library and class name
# (e.g., `pandas.DataFrame`, `polars.Series`).

# %%
import itables

itables.init_notebook_mode()

# %% [markdown]
# You can change this behavior globally with:
# ```python
# itables.options.show_df_type = True
# ```
#
# Or locally by passing `show_df_type=True` to the `show` function:

# %%
itables.show(itables.sample_dfs.get_countries(), show_df_type=True)
