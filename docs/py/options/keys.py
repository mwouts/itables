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
# # Keys
#
# With the [KeyTable](https://datatables.net/extensions/keytable/) extension you can navigate in a table using the arrow keys:

# %% tags=["full-width"]
import itables

itables.init_notebook_mode()

itables.show(
    itables.sample_dfs.get_countries(html=False),
    keys=True,
)

# %% [markdown]
# ```{tip}
# You can activate this option for all your tables with
#
# ~~~python
# itables.options.keys = True
# ~~~
# ```
#
# ```{warning}
# The KeyTable extension works in Jupyter Book (try it here in the documentation) but not in JupyterLab.
# ```
