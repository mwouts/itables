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
# # Column Visibility
#
# The [column visibility](https://datatables.net/extensions/buttons/examples/column_visibility/index.html) buttons of DataTables let you select which columns are visible.

# %% tags=["full-width"]
import itables

itables.init_notebook_mode()

df = itables.sample_dfs.get_countries()

itables.show(
    # column visibility works best with a flat header
    df.reset_index(),
    buttons=["columnsToggle"],
)

# %% [markdown]
# ```{tip}
# The column visibility button is available under many forms.
#
# Check-out `buttons=["colvis"]` for a [single](https://datatables.net/extensions/buttons/examples/column_visibility/simple.html) button.
#
# Extend the `colvis` button with the [collection layout](https://datatables.net/extensions/buttons/examples/column_visibility/layout.html).
#
# As always, when porting examples from DataTables to ITables, you will
# have to convert the JavaScript notation (left) to Python (right) as in the below:
# ::::{grid}
#
# :::{grid-item}
# :outline:
# :columns: 6
# ~~~javascript
# buttons: [
#     {
#         extend: 'colvis',
#         collectionLayout: 'fixed columns',
#         popoverTitle: 'Column visibility control'
#     }
# ]
# ~~~
# :::
# :::{grid-item}
# :outline:
# :columns: 6
# ~~~python
# buttons = [
#     {
#         "extend": "colvis",
#         "collectionLayout": "fixed columns",
#         "popoverTitle": "Column visibility control"
#     }
# ]
# ~~~
# :::
#
# ::::
#
# ```
