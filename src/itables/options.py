"""
Default options for ITables.

These parameters are documented at
https://itables.org/options/options.html
"""

import sys
from pathlib import Path
from types import ModuleType
from typing import Any, Literal, Mapping, Optional, Sequence, Union

import itables.config as config
import itables.typing as typing
import itables.utils as utils

__non_options = set(locals())

"""Table layout, see https://datatables.net/reference/option/layout
NB: to remove a control, replace it by None"""
layout: Mapping[str, Union[None, str, Mapping[str, Any]]] = {
    "topStart": "pageLength",
    "topEnd": "search",
    "bottomStart": "info",
    "bottomEnd": "paging",
}

"""
Show the index? Possible values: True, False and 'auto'. In mode 'auto', the index is not shown
if it has no name and its content is range(N)
"""
showIndex: Union[bool, Literal["auto"]] = "auto"

"""
Show the column data types? Possible values: True, False and 'auto'. In mode
'auto' the dtypes will be shown only for Polars dataframes, unless the
Polars config says otherwise.
"""
show_dtypes: Union[bool, Literal["auto"]] = "auto"

"""
Show the DataFrame or Series type, e.g. 'pandas.Series', 'polars.DataFrame', ...
"""
show_df_type: bool = False

"""
The default classes.
See https://itables.org/options/classes.html
"""
classes: Union[str, Sequence[str]] = "display nowrap compact"

"""
The default table style.
See https://itables.org/options/style.html

Use
- 'table-layout:auto' to compute the layout automatically
- 'width:auto' to fit the table width to its content
- 'margin:auto' to center the table.
Combine multiple options using ';'.

NB: When scrollX=true, "margin:auto" is replaced with "margin:0"
to avoid an issue with misaligned headers
"""
style: Union[str, dict[str, str]] = (
    "table-layout:auto;width:auto;margin:auto;caption-side:bottom"
)

"""
Custom CSS rules, e.g. '.dt-container { font-size: small; }'.

Unlike a standalone `display(HTML(f"<style>{css}</style>"))` cell, this CSS is embedded
in the output of every table, so it is guaranteed to render together with the table itself
(some notebook front-ends, like VS Code, defer the rendering of outputs that are scrolled
out of view, see https://github.com/mwouts/itables/issues/572).
"""
css: str = ""

"""Maximum bytes before downsampling a table"""
maxBytes: Union[str, int] = "64KB"

"""Maximum number of rows or columns before downsampling a table"""
maxRows: int = 0
maxColumns: int = 200

"""By default we don't sort the table"""
order: Optional[
    Union[Sequence[Sequence[Union[int, str]]], Mapping[str, Union[int, str]]]
] = []

"""
Should float values be formatted using the native Python DataFrame formatters?

Use 'auto' to format floats in Python only when the corresponding columns have
no render function defined in the DataTables columnDefs option.
"""
format_floats_in_python: Union[bool, Literal["auto"]] = "auto"

"""Should categorical columns be sorted according to the category order?

Use 'auto' to add rank-based sorting for categorical columns only when the
corresponding columns have no render function defined in the DataTables columnDefs
option. Set to False to sort categories alphabetically by DataTables.
"""
add_rank_to_categories: Union[bool, Literal["auto"]] = "auto"

"""Authorize, or not, the use of HTML in the table content.

Make sure that you trust the content of your tables before
setting this option to True.
"""
allow_html: bool = False

"""Optional table footer"""
footer: bool = False

"""Column filters"""
column_filters: Literal[False, "header", "footer"] = False

"""Should a warning appear when we have to encode an unexpected type?"""
warn_on_unexpected_types: bool = True

"""Should a warning appear when the selection targets rows that have been
filtered by the downsampling?"""
warn_on_selected_rows_not_rendered: bool = True

"""Display a warning if the private Polars formatting method is not found"""
warn_on_polars_get_fmt_not_found: bool = True

"""The DataTables URL for the connected mode"""
dt_url: str = utils.UNPKG_DT_BUNDLE_URL

"""The DataTable bundle for the offline mode
(this option is for 'init_notebook_mode')"""
dt_bundle: Union[str, Path] = utils.find_package_file("html/dt_bundle.js")

"""Display the ITables animated logo when loading"""
display_logo_when_loading: bool = True

"""Make the text in the table header selectable. When False, clicking
on the column header will sort the table. See #227"""
text_in_header_can_be_selected: bool = True

# these options are here just
# to document the corresponding types, see e.g. #224
caption: Optional[str]
lengthMenu: Optional[
    Union[
        Sequence[Union[int, str, Mapping[str, Any]]],
        Sequence[Sequence[Union[int, str]]],
    ]
]
pageLength: Optional[int]
columnDefs: Optional[Sequence[Mapping[str, Any]]]
paging: Optional[bool]
autoWidth: Optional[bool]
scrollX: Optional[bool]
scrollY: Optional[str]
scrollCollapse: Optional[bool]
language: Optional[Mapping[str, str]]
search: Optional[Mapping[str, Any]]
searchCols: Optional[Sequence[Any]]
initComplete: Optional[typing.JavascriptFunction]
fnInfoCallback: Optional[typing.JavascriptFunction]
drawCallback: Optional[typing.JavascriptFunction]
stateSave: Optional[bool]
stateDuration: Optional[int]
deferRender: Optional[bool]
buttons: Optional[Sequence[Union[str, Mapping[str, Any]]]]
colReorder: Optional[Union[bool, Mapping[str, Any]]]
scroller: Optional[Union[bool, Mapping[str, Any]]]
columnControl: Optional[Any]
fixedColumns: Optional[Mapping[Literal["left", "right", "start", "end"], int]]
fixedHeader: Optional[
    Union[
        bool,
        Mapping[
            Literal["header", "footer", "headerOffset", "footerOffset"],
            Union[bool, int, typing.JavascriptFunction],
        ],
    ]
]
searchPanes: Optional[Mapping[str, Any]]
searchBuilder: Optional[Mapping[str, Any]]
rowGroup: Optional[Mapping[str, Any]]
select: Optional[Union[bool, str, Mapping[str, str]]]
keys: Optional[bool]

warn_on_undocumented_option: bool = True
warn_on_unexpected_option_type: bool = (
    warn_on_undocumented_option and typing.is_typeguard_available()
)

"""Load the config file, if any"""
config.set_options_from_config_file(locals())

"""Check that options have correct names"""
if warn_on_undocumented_option:
    typing.check_itable_argument_names(
        {k for k in set(locals()).difference(__non_options) if not k.startswith("_")},
        typing.ITableOptions,
    )

"""Check that options have correct types"""
if warn_on_unexpected_option_type:
    typing.check_itable_argument_types(
        {
            k: v
            for k, v in locals().items()
            if k not in __non_options and not k.startswith("_")
        },
        typing.ITableOptions,
    )

_non_options = __non_options


class _ITableOptionsModule(ModuleType):
    """The class of the itables.options module.

    Options set on this module are checked as they are assigned, so that
    e.g. a typo in an option name, or an option with an unexpected type,
    is reported at the assignment rather than (possibly) much later, when
    a table is rendered ([#601](https://github.com/mwouts/itables/issues/601)).
    """

    def __setattr__(self, name: str, value: Any) -> None:
        super().__setattr__(name, value)
        if name.startswith("_") or name in _non_options:
            return
        if getattr(self, "warn_on_undocumented_option", False):
            typing.check_itable_argument_names({name}, typing.ITableOptions)
        if getattr(self, "warn_on_unexpected_option_type", False):
            typing.check_itable_argument_types({name: value}, typing.ITableOptions)


sys.modules[__name__].__class__ = _ITableOptionsModule
