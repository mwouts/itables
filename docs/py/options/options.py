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
# # Options
#
# ## DataTable Options
#
# ITables is a wrapper for the Javascript DataTables library, which means that you can use more or less directly the DataTables [options](https://datatables.net/options) from within Python.
#
# Since ITables just maps these options to DataTables, you are invited to have a look at DataTable's great [documentation](https://datatables.net/), and to its huge collection of [examples](https://datatables.net/examples/index). The DataTable [forum](https://datatables.net/forums/) can be quite useful as well.
#
# A non-exhaustive list of the DataTable options, together with their expected types, is available at [`itables.typing.DataTableOptions`](https://github.com/mwouts/itables/blob/main/src/itables/typing.py).
#
# Option names and types are checked by default at run time when `typeguard>=4.4.1` is installed - you can deactivate this by setting `warn_on_undocumented_option=False`.
#
# If you see an option that you find useful and is not documented, or a type hint that is incorrect, please make a PR (and add an example to the documentation, too).

# %% tags=["scroll-output"]
import inspect

import itables

print(inspect.getsource(itables.typing.DataTableOptions))

# %% [markdown]
# ## ITable Options
#
# ITables itself adds a few options like `connected`, `maxBytes`, `allow_html` etc.
#
# The ITable options are documented at [`itables.typing.ITableOptions`](https://github.com/mwouts/itables/blob/main/src/itables/typing.py):

# %% tags=["scroll-output"]
print(inspect.getsource(itables.typing.ITableOptions))

# %% [markdown]
# ## Default values
#
# Some of the options have a default value set in [`itables.options`](https://github.com/mwouts/itables/blob/main/src/itables/options.py). You can change these defaults easily, and even set defauts for the options that don't have one yet with e.g.
#
# ```python
# import itables
#
# itables.options.maxBytes = "128KB"
# ```

# %% tags=["scroll-output"]
print(inspect.getsource(itables.options))
