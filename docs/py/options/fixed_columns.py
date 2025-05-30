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
# # FixedColumns
#
# [FixedColumn](https://datatables.net/extensions/fixedcolumns/) is an extension
# that let you fix some columns as you scroll horizontally.

# %%
import string

import numpy as np
import pandas as pd

import itables

itables.init_notebook_mode()

wide_df = pd.DataFrame(
    {
        letter: np.random.normal(size=100)
        for letter in string.ascii_lowercase + string.ascii_uppercase
    }
)

itables.show(
    wide_df,
    fixedColumns={"start": 1, "end": 2},
    scrollX=True,
)
