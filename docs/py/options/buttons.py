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
# # Buttons
#
# The DataTables [buttons](https://datatables.net/extensions/buttons/) let you copy the table data, or export it as CSV or Excel files.
#
# To display the buttons, you need to pass a `buttons` argument to the `show` function:

# %% tags=["full-width"]
import itables

itables.init_notebook_mode()

df = itables.sample_dfs.get_countries()

itables.show(df, buttons=["pageLength", "copyHtml5", "csvHtml5", "excelHtml5"])

# %% [markdown]
# You can also specify a [`layout`](layout) modifier that will decide
# the location of the buttons (the default is `layout={"topStart": "buttons"}`). And if you want to keep the pagination control too, you can add `"pageLength"` to the list of buttons - as done above.
#
# As always, it is possible to set default values for these parameters by setting these on `itables.options`. For instance, set
# ```python
# itables.options.buttons = ["pageLength", "copyHtml5", "csvHtml5", "excelHtml5"]
# ```
# to get the buttons for all your tables.
#
# You can also add
# ```
# buttons = ["pageLength", "copyHtml5", "csvHtml5", "excelHtml5"]
# ```
# to your `itables.toml` configuration file.
#
#
# By default, the exported file name is the name of the HTML page. To change it, set a
# [`title` option](https://datatables.net/extensions/buttons/examples/html5/filename.html) on the buttons, like
# here:

# %% tags=["full-width"]
itables.show(
    df,
    buttons=[
        "pageLength",
        {"extend": "csvHtml5", "title": "download_filename"},
        {"extend": "excelHtml5", "title": "download_filename"},
    ],
)

# %% [markdown]
# ```{tip}
# Only the filtered or selected rows are exported to CSV/Excel. To filter the rows you can use the simple search box, the [SearchPanes](search_panes) and [SearchBuilder](search_builder) options, or the [select](select.md) extension.
# ```
#
# ```{warning}
# At the moment, the CSV and Excel buttons don't work well with large tables in some browsers.
# Please subscribe to [#251](https://github.com/mwouts/itables/issues/251) if you wish to receive updates on this.
# ```
#
# ```{warning}
# The PDF button is not included in ITables' DataTable bundle. This is because the required PDF libraries have a large footprint on the bundle size. Still, you can add it to your custom bundle, see our page on how to bundle [custom extensions](../custom_extensions.md).
# ```
