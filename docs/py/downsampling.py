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
# # Downsampling
#
# When an interactive table is displayed by `itables`, the table data is embedded in the notebook output. As we don't want your notebook to become super heavy just because you displayed a large table, we have a downsampling mechanism in place.
#
# When the data in a table is larger than `maxBytes`, which is equal to 64KB by default, `itables` will display only a subset of the table - one that fits into `maxBytes`, and display a warning that points to the `itables` documentation.
#
# If you wish, you can increase the value of `maxBytes` or even deactivate the limit (with `maxBytes=0`). Similarly, you can set a limit on the number of rows (`maxRows`, defaults to 0) or columns (`maxColumns`, defaults to `200`).

# %%
import itables

itables.init_notebook_mode()

# %%
itables.options.lengthMenu = [2, 5, 10, 20, 50, 100, 200, 500]
itables.options.maxBytes = "8KB"

df = itables.sample_dfs.get_indicators()
itables.downsample.as_nbytes(itables.options.maxBytes), itables.downsample.nbytes(df)

# %% tags=["full-width"]
df

# %% [markdown]
# To show the table in full, we can modify the value of `maxBytes` either locally:

# %% tags=["full-width"]
itables.show(df, maxBytes=0)

# %% [markdown]
# or globally:

# %% tags=["full-width"]
itables.options.maxBytes = "1MB"
df
