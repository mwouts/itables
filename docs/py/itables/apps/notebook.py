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
# # Notebook Mode
#
# Activate ITables in a Jupyter environment for all your tables with `init_notebook_mode`:

# %%
import itables

itables.init_notebook_mode()

# %% [markdown]
# You can go back to the standard HTML representation of Pandas DataFrames with `init_notebook_mode(all_interactive=False)`.

# %% tags=["full-width"]
df = itables.sample_dfs.get_countries()
df

# %% [markdown]
# Note that the `init_notebook_mode` function also activates ITables' offline mode, unless you call it with a `connected=False` argument.
#
#
# ## Offline mode
#
# By default `init_notebook_mode` configures ITables to work offline (except in Colab). No internet connection is required as the JavaScript code is embedded into the notebook itself when you execute `init_notebook_mode`.
#
# In some contexts (Jupyter Book, Google Colab, etc...) you might
# prefer to load the libraries dynamically from the internet.
# To do so, add the argument `connected=True` when you
# execute `init_notebook_mode`. This will also make your notebook lighter by
# about [900kB](https://github.com/mwouts/itables/blob/main/tests/test_connected_notebook_is_small.py). Note that, in Google Colab, `connected=True` is the only working option.
#
# ## Show
#
# If you prefer to render only certain tables using `itables`, or want to set additional options, use `show`:

# %% tags=["full-width"]
itables.show(df, caption="A DataFrame rendered with ITables")
