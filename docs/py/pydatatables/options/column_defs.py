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
# pyright: reportUnusedExpression=false

# %% [markdown]
# # Column Definitions
#
# The [`columnDefs.width`](https://datatables.net/reference/option/columns.width) argument let you adjust the column widths.
#
# Note that the default value of `style`, or of `autoWidth` (defaults to `True`), might override custom column widths,
# so you might have to change their values as in the examples below.
#
# You can set a fixed width for all the columns with `"targets": "_all"`:

# %% tags=["full-width"]
import itables

itables.init_notebook_mode()

df = itables.sample_dfs.get_countries()

itables.show(
    df,
    columnDefs=[{"width": "120px", "targets": "_all"}],
    style="width:1200px",
    autoWidth=False,
)

# %% [markdown]
# You can also adjust the width of selected columns only:

# %% tags=["full-width"]
itables.show(
    df,
    columnDefs=[{"width": "30%", "targets": [2, 3]}],
    style="width:100%;margin:auto",
)

# %% [markdown]
# If you wish you can also set a value for `columnDefs` permanently in `itables.options` as demonstrated in the cell alignment example below.
#
# You can use the DataTables [cell classes](https://datatables.net/manual/styling/classes#Cell-classes) like `dt-left`, `dt-center`, `dt-right` etc. to set the cell alignment. Specify it for one table by using the `columnDefs` argument of `show`

# %% tags=["full-width"]
itables.show(df, columnDefs=[{"className": "dt-center", "targets": "_all"}])

# %% [markdown]
# or globally by setting `itables.options.columnDefs`:

# %% tags=["full-width"]
itables.options.columnDefs = [{"className": "dt-center", "targets": "_all"}]

df
