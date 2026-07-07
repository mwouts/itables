from pathlib import Path
from typing import (
    Any,
    Literal,
    Mapping,
    Sequence,
    TypedDict,
    Union,
)

from itables_core.typing import (
    DataFrameModuleName,
    DataFrameOrSeries,
    DataFrameTypeName,
    JavascriptCode,
    JavascriptFunction,
    NotRequired,
    TypeAlias,
    Unpack,
    check_documented_option_names,
    check_documented_option_types,
    get_dataframe_module_and_type_name,
    get_dataframe_module_name,
    get_dataframe_type_description,
)
from itables_core.typing import get_silence_msg as _get_silence_msg
from itables_core.typing import (
    is_typeguard_available,
)

__all__ = [
    "NotRequired",
    "TypeAlias",
    "Unpack",
    "DataFrameModuleName",
    "DataFrameTypeName",
    "DataFrameOrSeries",
    "JavascriptCode",
    "JavascriptFunction",
    "AgGridOptions",
    "PyAgGridOptions",
    "PyAgGridRendererOptions",
    "get_dataframe_module_and_type_name",
    "get_dataframe_module_name",
    "get_dataframe_type_description",
    "is_typeguard_available",
    "check_pyaggrid_arguments",
    "check_pyaggrid_argument_names",
    "check_pyaggrid_argument_types",
]


class AgGridOptions(TypedDict):
    """
    This structure provides a non-exhaustive list of options that can be
    passed to the AG Grid constructor. See
    https://www.ag-grid.com/javascript-data-grid/grid-options/
    for the corresponding documentation.
    """

    columnDefs: NotRequired[Sequence[Mapping[str, Any]]]
    defaultColDef: NotRequired[Mapping[str, Any]]
    autoSizeStrategy: NotRequired[Mapping[str, Any]]

    pagination: NotRequired[bool]
    paginationPageSize: NotRequired[int]
    paginationPageSizeSelector: NotRequired[Union[Sequence[int], bool]]
    paginationAutoPageSize: NotRequired[bool]

    domLayout: NotRequired[Literal["normal", "autoHeight", "print"]]
    rowHeight: NotRequired[int]
    headerHeight: NotRequired[int]
    animateRows: NotRequired[bool]

    rowSelection: NotRequired[Union[str, Mapping[str, Any]]]
    cellSelection: NotRequired[Union[bool, Mapping[str, Any]]]
    quickFilterText: NotRequired[str]

    getRowStyle: NotRequired[JavascriptFunction]
    getRowClass: NotRequired[JavascriptFunction]
    onGridReady: NotRequired[JavascriptFunction]
    onCellClicked: NotRequired[JavascriptFunction]
    onSelectionChanged: NotRequired[JavascriptFunction]

    localeText: NotRequired[Mapping[str, str]]
    suppressFieldDotNotation: NotRequired[bool]
    enableCellTextSelection: NotRequired[bool]


class PyAgGridOptions(AgGridOptions):
    """
    A non-exhaustive list of options that can be passed
    to the pyaggrid 'show' and 'to_html_aggrid' functions.
    """

    classes: NotRequired[Union[str, Sequence[str]]]
    style: NotRequired[Union[str, dict[str, str]]]
    selected_rows: NotRequired[Sequence[int]]

    showIndex: NotRequired[Union[bool, Literal["auto"]]]
    show_df_type: NotRequired[bool]

    maxBytes: NotRequired[Union[int, str]]
    maxRows: NotRequired[int]
    maxColumns: NotRequired[int]

    table_id: NotRequired[str]
    ag_grid_url: NotRequired[str]
    ag_bundle: NotRequired[Union[str, Path]]
    theme: NotRequired[Literal["quartz", "balham", "material", "alpine"]]
    themeParams: NotRequired[Mapping[str, Any]]

    warn_on_unexpected_types: NotRequired[bool]
    warn_on_selected_rows_not_rendered: NotRequired[bool]
    warn_on_polars_get_fmt_not_found: NotRequired[bool]
    warn_on_undocumented_option: NotRequired[bool]
    warn_on_unexpected_option_type: NotRequired[bool]


class PyAgGridRendererOptions(TypedDict):
    """
    The arguments passed to the pyaggrid HTML template.
    """

    columns: NotRequired[Sequence[str]]
    data_json: NotRequired[str]
    grid_options: NotRequired[Mapping[str, Any]]

    caption: NotRequired[str]
    theme: NotRequired[str]
    downsampling_warning: NotRequired[str]
    keys_to_be_evaluated: NotRequired[Sequence[Sequence[Union[int, str]]]]


_OPTIONS_MODULE = "pyaggrid.options"


def get_silence_msg(option_name: str) -> str:
    return _get_silence_msg(option_name, _OPTIONS_MODULE)


def check_pyaggrid_arguments(kwargs: "dict[str, Any]", typed_dict: type) -> None:
    """
    Check the arguments passed to the pyaggrid functions
    """
    warn_on_undocumented_option = (
        kwargs.get if typed_dict is PyAgGridOptions else kwargs.pop
    )("warn_on_undocumented_option", False)

    warn_on_unexpected_option_type = (
        kwargs.get if typed_dict is PyAgGridOptions else kwargs.pop
    )("warn_on_unexpected_option_type", False)

    if warn_on_undocumented_option:
        check_pyaggrid_argument_names(set(kwargs), typed_dict)

    if warn_on_unexpected_option_type:
        check_pyaggrid_argument_types(kwargs, typed_dict)


def check_pyaggrid_argument_names(names: "set[str]", typed_dict: type) -> None:
    """
    Check that the arguments passed to the pyaggrid functions
    are documented in the given TypedDict.
    """
    check_documented_option_names(names, typed_dict, _OPTIONS_MODULE)


def check_pyaggrid_argument_types(kwargs: "dict[str, Any]", typed_dict: type) -> None:
    """
    Check that the arguments passed to the pyaggrid functions
    match the types defined in the given TypedDict.
    """
    check_documented_option_types(kwargs, typed_dict, _OPTIONS_MODULE)
