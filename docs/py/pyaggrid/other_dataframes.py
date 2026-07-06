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
# ruff: noqa: E402
# pyright: reportUnusedExpression=false

# %% [markdown]
# # Other DataFrames
#
# PyAgGrid can render other types of DataFrames than Pandas and Polars
# if you have [Narwhals](https://narwhals-dev.github.io/narwhals/) installed.
# If you would like to see more examples DataFrames here, please reach
# out to us on [GitHub](https://github.com/mwouts/itables).

# %% tags=["remove-cell"]
# pyright: reportMissingTypeStubs=false
# pyright: reportUnknownMemberType=false

# %%
import modin.pandas as mpd
import pyaggrid
import pyarrow as pa

# %% [markdown]
# ## PyArrow

# %%
pyaggrid.show(pa.table({"A": [1, 2, 3], "B": [4.1, 5.2, 6.3]}))

# %% [markdown]
# ## Modin

# %%
pyaggrid.show(mpd.DataFrame({"A": [1, 2, 3], "B": [4.1, 5.2, 6.3]}))
