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
# # Column Control
#
# The [`columnControl`](https://datatables.net/extensions/columncontrol/config) option lets you add column specific controls.
#
# The examples should give you a quick sense of how to use `columnControl`. You are invited to consult the datatables documentation for many more column control [examples](https://datatables.net/extensions/columncontrol/examples/) - see also Allan's [post](https://datatables.net/blog/2025/columncontrol) in which the extension was introduced.

# %% tags=["full-width"]
import itables

itables.init_notebook_mode()

df = itables.sample_dfs.get_countries()

# %% [markdown]
# ## Getting started
#
# The `columnControl` option can take as value the list of controls that should be added to the table columns.

# %%
itables.show(
    df,
    columnControl=["order", "colVisDropdown", "searchDropdown"],
    ordering={"indicators": False, "handler": False},
)

# %% [markdown]
# ```{tip}
# When an ordering option is provided through the `columnControl` option,
# you probably want to deactivate the default ordering icons - that's the purpose of
# `ordering={"indicators": False, "handler": False}` used in the example above.
# ```
#
# ## Drop-downs
#
# Nested lists are mapped to dropdowns:

# %%
itables.show(
    df,
    columnControl=["order", ["orderAsc", "orderDesc", "search"]],
    ordering={"indicators": False, "handler": False},
)

# %% [markdown]
# ## Controls and table footers
#
# The column controls can also be added to a table footer:

# %%
itables.show(
    df,
    columnControl=[
        {"target": 0, "content": ["order"]},
        {"target": "tfoot", "content": ["search"]},
    ],
    ordering={"indicators": False, "handler": False},
)
