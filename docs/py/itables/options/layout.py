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
# # Layout
#
# By default, datatables that don't fit in one page come with a search box, a pagination control, a table summary, etc.
# You can select which elements are actually displayed using
# DataTables' [`layout` option](https://datatables.net/reference/option/layout) with e.g.:

# %%
import itables

itables.init_notebook_mode()
df = itables.sample_dfs.get_countries()

# %%
itables.show(df, layout={"topStart": "search", "topEnd": None})

# %% [markdown]
# The available positions are `topStart, topEnd, bottomStart, bottomEnd`. You can also use `top2Start`, etc... (see more
# in the [DataTables documentation](https://datatables.net/reference/option/layout)).
#
# Like for the other arguments of `show`, you can change the default value of the dom option with e.g.:
#
# ```
# itables.options.layout =  {
#     "topStart": "pageLength",
#     "topEnd": "search",
#     "bottomStart": "info",
#     "bottomEnd": "paging"
# }  # (default value)
# ```
#
# ```{tip}
# The `layout` option was introduced with `itables==2.0` and `DataTables==2.0`
# and replaced the former [`dom` option](https://datatables.net/reference/option/dom).
# ```
