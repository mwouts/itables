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
# # FixedHeader
#
# [FixedHeader](https://datatables.net/extensions/fixedheader/) is a DataTables extension
# that keeps the table header visible while scrolling.
#
# Use `fixedHeader=True` to enable a fixed table header:

# %% tags=["full-width"]
import itables

itables.init_notebook_mode()

df = itables.sample_dfs.get_countries()

itables.show(
    df,
    # fixedHeader=True is simpler,
    # but in some contexts, like here in Jupyter Book,
    # we need to account for the other fixed elements
    fixedHeader={"header": True, "headerOffset": 48},
)

# %% [markdown]
# You can also configure header and footer behavior explicitly, as in the
# [header/footer example](https://datatables.net/extensions/fixedheader/examples/options/header_footer.html):

# %% tags=["full-width"]
itables.show(
    df,
    footer=True,
    fixedHeader={"header": True, "footer": True},
)

# %% [markdown]
# As always, you can set this option globally with:
# ```python
# itables.options.fixedHeader = True
# ```
#
# or by adding
# ```
# fixedHeader = true
# ```
# to your [`itables.toml` configuration file](../configuration.md).
