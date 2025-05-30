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
# # Marimo
#
# ```{warning}
# The `init_notebook_mode` and the `show` function do not work in Marimo. This is because they both use `IPython.display` to display the HTML representation of the table, which is not a good fit for Marimo.
# ```
#
# In Marimo the recommended way to use ITable is through the `ITable` [widget](widget.md):

# %%
import pandas as pd

from itables.widget import ITable

df = pd.DataFrame({"x": [2, 1, 3]})

ITable(df)

# %% [markdown]
# A Sample Marimo application is available at [`apps/marimo/widget.py`](https://github.com/mwouts/itables/tree/main/apps/marimo/widget.py).
#
#
# ## Using HTML
#
# You can also use `to_html_datatable` in combination with `mo.iframe` like in this example - but, as there is no `init_notebook_mode` cell, you will have to use the connected mode:
#
# ```python
# import marimo as mo
#
# from itables import to_html_datatable
#
# html = to_html_datatable(df, connected=True)
# mo.iframe(html)
# ```
#
# A Sample Marimo application that uses `to_html_datatable` is available at [`apps/marimo/html.py`](https://github.com/mwouts/itables/tree/main/apps/marimo/html.py).
