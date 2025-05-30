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
# # Search Panes
#
# [SearchPanes](https://datatables.net/extensions/searchpanes/) is an extension that lets you select rows based on unique values. In the example below we have activated the cascade filtering through the [`searchPanes.cascadePanes`](https://datatables.net/extensions/searchpanes/examples/initialisation/cascadePanes.html) argument.
#
# Note that, in Jupyter, the [`searchPanes.layout`](https://datatables.net/extensions/searchpanes/layout) argument is required (otherwise the search panes are too wide).

# %% tags=["full-width"]
import itables

itables.init_notebook_mode()

df = itables.sample_dfs.get_countries(html=False, climate_zone=True)

itables.show(
    df.reset_index(),
    layout={"top1": "searchPanes"},
    searchPanes={"layout": "columns-3", "cascadePanes": True, "columns": [1, 6, 7]},
)

# %% [markdown]
# ```{warning}
# When searching, please keep in mind that ITables will [downsample](../downsampling.md) your table if it is larger than `maxBytes`, so you might not see the full dataset - pay attention to the downsampling message at the bottom left of the table.
# ```
