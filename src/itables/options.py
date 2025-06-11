"""
Default options for ITables.

These parameters are documented at
https://mwouts.github.io/itables/options/options.html
"""

from pathlib import Path
from typing import Any, Literal, Mapping, Optional, Sequence, Union

import itables.typing as typing
import itables.utils as utils

__non_options = set()
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
showIndex: Literal[True, False, "auto"] = "auto"

"""
The default classes.
See https://mwouts.github.io/itables/options/classes.html
"""
classes: Union[str, Sequence[str]] = "display nowrap"

"""
The default table style.
See https://mwouts.github.io/itables/options/style.html

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

"""Maximum bytes before downsampling a table"""
maxBytes: Union[str, int] = "64KB"

"""Maximum number of rows or columns before downsampling a table"""
maxRows: int = 0
maxColumns: int = 200

"""By default we don't sort the table"""
order: Optional[
    Union[Sequence[Sequence[Union[int, str]]], Mapping[str, Union[int, str]]]
] = []

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
buttons: Optional[Sequence[Union[str, Mapping[str, Any]]]]
fixedColumns: Optional[Mapping[Literal["left", "right", "start", "end"], int]]
searchPanes: Optional[Mapping[str, Any]]
searchBuilder: Optional[Mapping[str, Any]]
rowGroup: Optional[Mapping[str, Any]]
select: Optional[Union[bool, str, Mapping[str, str]]]
keys: Optional[bool]

"""Check that options have correct names"""
warn_on_undocumented_option: bool = True
if warn_on_undocumented_option:
    typing.check_itable_argument_names(
        set(locals()).difference(__non_options),
        typing.ITableOptions,
    )

"""Check that options have correct types"""
warn_on_unexpected_option_type: bool = (
    warn_on_undocumented_option and typing.is_typeguard_available()
)
if warn_on_unexpected_option_type:
    typing.check_itable_argument_types(
        {k: v for k, v in locals().items() if k not in __non_options},
        typing.ITableOptions,
    )
