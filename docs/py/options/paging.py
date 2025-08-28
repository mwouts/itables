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
# # Paging
#
# Use [`paging=False`](https://datatables.net/reference/option/paging) to show the table in full:

# %%
import itables

itables.init_notebook_mode()
df = itables.sample_dfs.get_countries()

# %% tags=["full-width"]
itables.show(df.head(8), paging=False)
