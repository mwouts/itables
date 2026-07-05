# ---
# jupyter:
#   jupytext:
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
# The `init_notebook_mode` and the `show` functions do not work in Marimo. This is because they both use `IPython.display` to display the HTML representation of the table, which is not a good fit for Marimo.
# ```
#
# In Marimo the recommended way to use PyAgGrid is through the `AgGrid`
# [widget](widget.md):
#
# ```python
# import pandas as pd
#
# from pyaggrid.widget import AgGrid
#
# df = pd.DataFrame({"x": [2, 1, 3]})
#
# AgGrid(df)
# ```
#
# A sample Marimo application is available at
# [`apps/pyaggrid/marimo/app.py`](https://github.com/mwouts/itables/tree/main/apps/pyaggrid/marimo/app.py).
#
# ## Using HTML
#
# You can also use `to_html_aggrid` in combination with `mo.iframe`:
#
# ```python
# import marimo as mo
#
# from pyaggrid import to_html_aggrid
#
# html = to_html_aggrid(df)
# mo.iframe(html)
# ```
