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
# # State Save
#
# To preserve the table state, like the [selected columns](colvis.md) or the [row order](order.md) you can use the [`stateSave`](https://datatables.net/reference/option/stateSave) option. This will preserve the table state when the page is reloaded, or when an ITable component is updated.
#
# ```{tip}
# You might also want to adjust [`stateDuration`](https://datatables.net/reference/option/stateDuration) which defaults to 2 hours.
# ```
#
# Try the option on this page: re-order the table by clicking on one column, then refresh the page - the order will be preserved.

# %% tags=["full-width"]
import itables

itables.init_notebook_mode()

df = itables.sample_dfs.get_countries()

itables.show(df, stateSave=True)
