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
# # Caption

# %% tags=["full-width"]
import itables

itables.init_notebook_mode()

df = itables.sample_dfs.get_countries(html=False)
itables.show(df, "Countries from the World Bank Database")

# %% [markdown]
# The caption appears at the bottom of the table by default: this is governed by `caption-side:bottom`
# in the [`style` option](style) (but for some reason this is not effective in Jupyter Book 🤔).
