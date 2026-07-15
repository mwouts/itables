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
# # Static preview - Polars dataframes
#
# `itables.to_html_static_preview()` returns the plain HTML table that
# `to_html_datatable()` embeds in a `<noscript>` tag - see
# [Static preview](static_preview.md) for why, and when, this is shown
# instead of the interactive table. This page shows it for each of our test
# [Polars](https://www.pola.rs/) dataframes; see
# [Polars dataframes](../polars_dataframes.md) for the same dataframes rendered
# as interactive tables.

# %%
from IPython.display import HTML, display

import itables

dict_of_test_dfs = itables.sample_polars_dfs.get_dict_of_test_dfs()

# %% [markdown]
# ## empty

# %%
display(HTML(itables.to_html_static_preview(dict_of_test_dfs["empty"])))

# %% [markdown]
# ## No rows

# %%
display(HTML(itables.to_html_static_preview(dict_of_test_dfs["no_rows"])))

# %% [markdown]
# ## bool

# %%
display(HTML(itables.to_html_static_preview(dict_of_test_dfs["bool"])))

# %% [markdown]
# ## Nullable boolean

# %%
display(HTML(itables.to_html_static_preview(dict_of_test_dfs["nullable_boolean"])))

# %% [markdown]
# ## int

# %%
display(HTML(itables.to_html_static_preview(dict_of_test_dfs["int"])))

# %% [markdown]
# ## Nullable integer

# %%
display(HTML(itables.to_html_static_preview(dict_of_test_dfs["nullable_int"])))

# %% [markdown]
# ## float

# %%
display(HTML(itables.to_html_static_preview(dict_of_test_dfs["float"])))

# %% [markdown]
# ## float_types

# %%
display(HTML(itables.to_html_static_preview(dict_of_test_dfs["float_types"])))

# %% [markdown]
# ## str

# %%
display(HTML(itables.to_html_static_preview(dict_of_test_dfs["str"])))

# %% [markdown]
# ## time

# %%
display(HTML(itables.to_html_static_preview(dict_of_test_dfs["time"])))

# %% [markdown]
# ## date_range

# %%
display(HTML(itables.to_html_static_preview(dict_of_test_dfs["date_range"])))

# %% [markdown]
# ## ordered_categories

# %%
display(HTML(itables.to_html_static_preview(dict_of_test_dfs["ordered_categories"])))

# %% [markdown]
# ## object

# %%
display(HTML(itables.to_html_static_preview(dict_of_test_dfs["object"])))

# %% [markdown]
# ## countries

# %% tags=["full-width"]
display(HTML(itables.to_html_static_preview(dict_of_test_dfs["countries"])))

# %% [markdown]
# ## int_float_str

# %%
display(HTML(itables.to_html_static_preview(dict_of_test_dfs["int_float_str"])))

# %% [markdown]
# ## wide

# %% tags=["full-width"]
display(HTML(itables.to_html_static_preview(dict_of_test_dfs["wide"])))

# %% [markdown]
# ## long_column_names

# %% tags=["full-width"]
display(HTML(itables.to_html_static_preview(dict_of_test_dfs["long_column_names"])))

# %% [markdown]
# ## big_integers

# %%
display(HTML(itables.to_html_static_preview(dict_of_test_dfs["big_integers"])))
