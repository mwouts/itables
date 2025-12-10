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
# pyright: reportUnknownMemberType=false

# %% [markdown]
# # RowGroup
#
# Use the [RowGroup](https://datatables.net/extensions/rowgroup/) extension to group
# the data according to the content of one colum. Optionally, you can hide the content of that column to avoid duplicating the information.

# %% tags=["full-width"]
import itables

itables.init_notebook_mode()

df = itables.sample_pandas_dfs.get_countries()

itables.show(
    df.sort_values("region"),
    rowGroup={"dataSrc": 1},
    columnDefs=[{"targets": 1, "visible": False}],
)
