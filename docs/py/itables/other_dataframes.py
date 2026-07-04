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
# # Other DataFrames
#
# ITables can render other types of DataFrames than Pandas and Polars
# if you have [Narwhals](https://narwhals-dev.github.io/narwhals/) installed.
# If you would like to see more examples DataFrames here, please reach
# out to us on [GitHub](https://github.com/mwouts/itables).

# %% tags=["remove-cell"]
# pyright: reportMissingTypeStubs=false
# pyright: reportUnknownMemberType=false

# %%
import modin.pandas as mpd
import pyarrow as pa

import itables

# %% [markdown]
# ## PyArrow

# %%
itables.show(pa.table({"A": [1, 2, 3], "B": [4.1, 5.2, 6.3]}))

# %% [markdown]
# # Modin

# %%
itables.show(mpd.DataFrame({"A": [1, 2, 3], "B": [4.1, 5.2, 6.3]}))
