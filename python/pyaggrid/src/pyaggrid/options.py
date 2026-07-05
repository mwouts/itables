"""
Default options for the pyaggrid tables.
"""

from typing import Any, Literal, Mapping, Optional, Sequence, Union

import pyaggrid.typing as typing
import pyaggrid.utils as utils

__non_options = set(locals())

"""
Show the index? Possible values: True, False and 'auto'. In mode 'auto', the index is not shown
if it has no name and its content is range(N)
"""
showIndex: Union[bool, Literal["auto"]] = "auto"

"""
Show the DataFrame or Series type, e.g. 'pandas.Series', 'polars.DataFrame', ...
"""
show_df_type: bool = False

"""
The default classes added to the grid container div.
"""
classes: Union[str, Sequence[str]] = "pyaggrid"

"""
The default style of the grid container div. Note that after the first
rendering, the width of the container is adjusted to the table content
(unless domLayout is set to 'normal').
"""
style: Union[str, dict[str, str]] = "width:100%"

"""Maximum bytes before downsampling a table"""
maxBytes: Union[str, int] = "64KB"

"""Maximum number of rows or columns before downsampling a table"""
maxRows: int = 0
maxColumns: int = 200

"""The AG Grid theme, one of 'quartz', 'balham', 'material' or 'alpine'"""
theme: Literal["quartz", "balham", "material", "alpine"] = "quartz"

"""Paginate the tables"""
pagination: bool = True
paginationPageSize: int = 20

"""The layout of the grid. With 'autoHeight' the grid height
adjusts to the number of displayed rows"""
domLayout: Literal["normal", "autoHeight", "print"] = "autoHeight"

"""The default column options, see
https://www.ag-grid.com/javascript-data-grid/column-definitions/"""
defaultColDef: Mapping[str, Any] = {"filter": True}

"""The URL of the AG Grid Community ESM bundle used in the connected mode"""
ag_grid_url: str = utils.AG_GRID_ESM_URL

"""Should a warning appear when we have to encode an unexpected type?"""
warn_on_unexpected_types: bool = True

"""Should a warning appear when the selection targets rows that have been
filtered by the downsampling?"""
warn_on_selected_rows_not_rendered: bool = True

"""Display a warning if the private Polars formatting method is not found"""
warn_on_polars_get_fmt_not_found: bool = True

# these options are here just
# to document the corresponding types
caption: Optional[str]
columnDefs: Optional[Sequence[Mapping[str, Any]]]
autoSizeStrategy: Optional[Mapping[str, Any]]
paginationPageSizeSelector: Optional[Union[Sequence[int], bool]]
paginationAutoPageSize: Optional[bool]
rowHeight: Optional[int]
headerHeight: Optional[int]
animateRows: Optional[bool]
rowSelection: Optional[Union[str, Mapping[str, Any]]]
cellSelection: Optional[Union[bool, Mapping[str, Any]]]
quickFilterText: Optional[str]
getRowStyle: Optional[typing.JavascriptFunction]
getRowClass: Optional[typing.JavascriptFunction]
onGridReady: Optional[typing.JavascriptFunction]
onCellClicked: Optional[typing.JavascriptFunction]
onSelectionChanged: Optional[typing.JavascriptFunction]
localeText: Optional[Mapping[str, str]]
suppressFieldDotNotation: Optional[bool]
enableCellTextSelection: Optional[bool]

warn_on_undocumented_option: bool = True
warn_on_unexpected_option_type: bool = (
    warn_on_undocumented_option and typing.is_typeguard_available()
)

"""Check that options have correct names"""
if warn_on_undocumented_option:
    typing.check_pyaggrid_argument_names(
        {k for k in set(locals()).difference(__non_options) if not k.startswith("_")},
        typing.PyAgGridOptions,
    )

"""Check that options have correct types"""
if warn_on_unexpected_option_type:
    typing.check_pyaggrid_argument_types(
        {
            k: v
            for k, v in locals().items()
            if k not in __non_options and not k.startswith("_")
        },
        typing.PyAgGridOptions,
    )
