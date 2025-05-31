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
# # Rendering Mathematical Formulae
#
# To render mathematical contents like equations in your DataFrame (rows or header), use the `render_math` option:

# %%
import pandas as pd

import itables

itables.init_notebook_mode()

itables.show(
    pd.DataFrame(
        {
            "$N_{\\text{event}}$": ["$\\alpha$", "$\\beta$", "$\\gamma$"] * 10,
            "Value": [
                "$0.8_{-0.1}^{+0.3}$",
                "$3.2_{-0.4}^{+0.2}$",
                "$-0.1_{-0.5}^{+0.8}$",
            ]
            * 10,
        }
    ),
    render_math=True,
)
