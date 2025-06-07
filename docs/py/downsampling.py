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

# %% tags=["remove-cell"]
# pyright: reportUnusedExpression=false

# %% [markdown]
# # Downsampling
#
# When an interactive table is displayed by `itables`, the table data is embedded into the notebook itself. Large tables need to be downsampled, otherwise your notebook will become huge and irresponsive.
#
# Downsampling occurs when the table data is larger than `maxBytes`, which is equal to 64KB by default. When downsampling occurs, a warning is displayed below the table, which points to the `itables` documentation.
#
# If you wish, you can increase the value of `maxBytes` or even deactivate the limit (with `maxBytes=0`) - but again, that will break your notebook when you display a large dataframe.
#
# Similarly, you can set a limit on the number of rows (`maxRows`, defaults to 0) or columns (`maxColumns`, defaults to `200`).

# %%
import itables

itables.init_notebook_mode()

# %% tags=["full-width"]
itables.options.maxBytes = "8KB"

df = itables.sample_dfs.get_countries(html=False)
itables.downsample.as_nbytes(itables.options.maxBytes), itables.downsample.nbytes(df)

# %% tags=["full-width"]
df

# %% [markdown]
# To show the table in full, we can modify the value of `maxBytes` either locally:

# %% tags=["full-width"]
itables.show(df, maxBytes=32768)

# %% [markdown]
# or globally:

# %% tags=["full-width"]
itables.options.maxBytes = "1MB"
df
