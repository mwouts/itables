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
# # Order
#
# Since ITables v1.3.0, the interactive datatable shows the rows in the same order as the original dataframe.
#
# You can pre-select a explicit order with the [`order`](https://datatables.net/reference/option/order) option:

# %%
import pandas as pd

import itables

itables.init_notebook_mode()

sorted_df = pd.DataFrame({"i": [1, 2], "a": [2, 1]}).set_index(["i"])
itables.show(sorted_df, order=[[1, "asc"]])
