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
# # Search
#
# The [search option](https://datatables.net/reference/option/search) let you control the initial value for the search field, and whether the query should be treated as a regular expression or not:

# %%
import itables

itables.init_notebook_mode()

# %% tags=["full-width"]
df = itables.sample_dfs.get_countries(html=False)
itables.show(df, search={"regex": True, "caseInsensitive": True, "search": "s.ain"})
