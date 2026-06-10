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
# # Vertical Scroll
#
# The [`scrollY`](https://datatables.net/examples/basic_init/scroll_y.html) parameter is an interesting alternative to the pagination:

# %% tags=["full-width"]
import itables

itables.init_notebook_mode()

df = itables.sample_dfs.get_countries()
itables.show(df, scrollY="350px", scrollCollapse=True, paging=False)

# %% [markdown]
# ## Scroller
#
# When `scrollY` is set, DataTables still renders every row of the current page into the
# page (and with `paging=False`, every row of the table). That is fine for small tables,
# but for large ones it is more efficient to render only the rows that are actually
# visible. This is what the [Scroller](https://datatables.net/extensions/scroller/)
# extension does: it implements *virtual scrolling*, so only the rows in (or near) the
# viewport exist in the DOM at any given time, while the scrollbar still represents the
# full table.
#
# To enable it, set `scroller=True` together with `scrollY`:

# %% tags=["full-width"]
itables.show(df, scroller=True, scrollY="350px")

# %% [markdown]
# ### Defer Render
#
# The `deferRender` option tells DataTables to only create the HTML for a row when it is
# first displayed. It pairs naturally with Scroller and further reduces the initial
# rendering cost for large tables:

# %% tags=["full-width"]
itables.show(df, scroller=True, scrollY="350px", deferRender=True)

# %% [markdown]
# ### Scroller options
#
# You can pass a dictionary to `scroller` to configure it further. For example,
# `loadingIndicator=True` shows a message while rows are being rendered:

# %% tags=["full-width"]
itables.show(df, scroller={"loadingIndicator": True}, scrollY="350px", deferRender=True)

# %% [markdown]
# As always, you can set these options globally with:
# ```python
# itables.options.scroller = True
# itables.options.deferRender = True
# ```
#
# or by adding
# ```
# scroller = true
# deferRender = true
# ```
# to your [`itables.toml` configuration file](../configuration.md).
