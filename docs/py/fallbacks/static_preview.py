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
# pyright: reportUnknownVariableType=false

# %% [markdown]
# # Static Preview
#
# ## Viewing a notebook with ITables tables on GitHub
#
# GitHub renders `.ipynb` files as non interactive HTML pages. If the notebook
# outputs contain JavaScript code, that code is not executed. Since ITables tables are
# normally interactive DataTables built with JavaScript, GitHub can't show
# them that way.
#
# To address this, ITables v2.9+ ships a **static preview** with every table: a plain HTML table with just the first rows - 10 by default, or as many as your
# `pageLength`/`lengthMenu` options say. GitHub shows that static preview
# instead of the interactive table.
#
# Untrusted notebooks, which can't use JavaScript until you trust them, also use the same fallback - see
# [Seeing a static preview instead?](../troubleshooting.md#seeing-a-static-preview-instead).
#
# ## What the fallback looks like
#
# `to_html_datatable` shows that static preview - built with
# `to_html_static_preview` - by default, right next to the interactive
# table, which starts out hidden. A small inline script swaps the two
# around wherever it actually gets to run (a real, JavaScript-capable
# session): a `<noscript>` tag would not do here, since it only hides its
# content when scripting is disabled for the whole page, which isn't the
# case on GitHub - GitHub's notebook preview is itself a JavaScript-powered
# page, it just doesn't execute the `<script>` tags in our output. Here is
# the static preview, the same plain HTML table you'd see on GitHub:

# %%
from IPython.display import HTML, display

import itables

df = itables.sample_dfs.get_countries()
display(HTML(itables.to_html_static_preview(df)))

# %% [markdown]
# ## An example notebook
#
# [static_preview_demo.ipynb](https://github.com/mwouts/itables/blob/main/tests/data/static_preview_notebooks/static_preview_demo.ipynb)
# is a small notebook, generated and executed as part of ITables' test suite,
# that demonstrates this fallback. Open it on GitHub to see the static
# preview tables, or download it and either run it, or trust it, to see the interactive tables instead.
