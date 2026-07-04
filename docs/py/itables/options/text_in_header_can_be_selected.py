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
# # Select Text in Header
#
# The `text_in_header_can_be_selected` option, which defaults to `True`, is provided by ITables since v2.4.0.
#
# With that option set (the default), you can select the text in the table headers. This is useful in the context of data exploration where
# you need to copy back the column name to your code.

# %%
import itables

itables.init_notebook_mode()
df = itables.sample_dfs.get_countries()

itables.show(df, "A table in which column headers can be selected")

# %% [markdown]
# When `text_in_header_can_be_selected=False`, the column title cannot be selected as clicking on the title sorts the table.

# %%
itables.show(
    df,
    "A table in which column headers cannot be selected",
    text_in_header_can_be_selected=False,
)
