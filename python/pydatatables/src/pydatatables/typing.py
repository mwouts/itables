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
    "DataTableOptions",
    "PyDataTablesOptions",
    "PyDataTablesRendererOptions",
    "get_dataframe_module_and_type_name",
    "get_dataframe_module_name",
    "get_dataframe_type_description",
    "is_typeguard_available",
    "check_itable_arguments",
    "check_itable_argument_names",
    "check_itable_argument_types",
]


class DataTableOptions(TypedDict):
    """
    This structure provides a non-exhaustive list of options that can be passed
    to the DataTable constructor. See https://datatables.net/reference/option/
    for the corresponding documentation.
    """

    # DataTable options
    lengthMenu: NotRequired[
        Union[
            Sequence[Union[int, str, Mapping[str, Any]]],
            Sequence[Sequence[Union[int, str]]],
        ]
    ]
    pageLength: NotRequired[int]
    order: NotRequired[
        Union[Sequence[Sequence[Union[int, str]]], Mapping[str, Union[int, str]]]
    ]
    layout: NotRequired[Mapping[str, Union[None, str, Mapping[str, Any]]]]
    columnDefs: NotRequired[Sequence[Mapping[str, Any]]]
    ordering: NotRequired[Union[bool, Mapping[str, bool]]]
    paging: NotRequired[bool]
    autoWidth: NotRequired[bool]
    scrollX: NotRequired[bool]
    scrollY: NotRequired[str]
    scrollCollapse: NotRequired[bool]
    language: NotRequired[Mapping[str, str]]
    search: NotRequired[Mapping[str, Any]]
    searchCols: NotRequired[Sequence[Any]]
    initComplete: NotRequired[JavascriptFunction]
    fnInfoCallback: NotRequired[JavascriptFunction]
    drawCallback: NotRequired[JavascriptFunction]
    stateSave: NotRequired[bool]
    stateDuration: NotRequired[int]
    deferRender: NotRequired[bool]

    # DataTable options provided by its extensions
    buttons: NotRequired[Sequence[Union[str, Mapping[str, Any]]]]
    colReorder: NotRequired[Union[bool, Mapping[str, Any]]]
    scroller: NotRequired[Union[bool, Mapping[str, Any]]]
    columnControl: NotRequired[Any]
    fixedColumns: NotRequired[Mapping[Literal["left", "right", "start", "end"], int]]
    fixedHeader: NotRequired[
        Union[
            bool,
            Mapping[
                Literal["header", "footer", "headerOffset", "footerOffset"],
                Union[bool, int, JavascriptFunction],
            ],
        ]
    ]
    searchPanes: NotRequired[Mapping[str, Any]]
    searchBuilder: NotRequired[Mapping[str, Any]]
    rowGroup: NotRequired[Mapping[str, Any]]
    select: NotRequired[Union[bool, str, Mapping[str, str]]]
    keys: NotRequired[bool]


class PyDataTablesOptions(DataTableOptions):
    """
    A non-exhaustive list of options that can be passed
    to the show function and to the PyDataTablesRenderer Python classes.
    """

    classes: NotRequired[Union[str, Sequence[str]]]
    style: NotRequired[Union[str, dict[str, str]]]
    selected_rows: NotRequired[Sequence[int]]

    showIndex: NotRequired[Union[bool, Literal["auto"]]]
    show_dtypes: NotRequired[Union[bool, Literal["auto"]]]
    show_df_type: NotRequired[bool]

    maxBytes: NotRequired[Union[int, str]]
    maxRows: NotRequired[int]
    maxColumns: NotRequired[int]

    allow_html: NotRequired[bool]
    format_floats_in_python: NotRequired[Union[bool, Literal["auto"]]]
    add_rank_to_categories: NotRequired[Union[bool, Literal["auto"]]]

    table_id: NotRequired[str]
    dt_url: NotRequired[str]
    dt_bundle: NotRequired[Union[str, Path]]
    connected: NotRequired[bool]
    display_logo_when_loading: NotRequired[bool]

    footer: NotRequired[bool]

    warn_on_unexpected_types: NotRequired[bool]
    warn_on_selected_rows_not_rendered: NotRequired[bool]
    warn_on_polars_get_fmt_not_found: NotRequired[bool]
    warn_on_undocumented_option: NotRequired[bool]
    warn_on_unexpected_option_type: NotRequired[bool]
    text_in_header_can_be_selected: NotRequired[bool]

    column_filters: NotRequired[Literal[False, "header", "footer"]]

    use_to_html: NotRequired[bool]


class PyDataTablesRendererOptions(DataTableOptions):
    """
    The options that can be passed to the PyDataTablesRenderer constructor
    in the pydatatables package.
    """

    caption: NotRequired[str]
    classes: NotRequired[Union[str, Sequence[str]]]
    style: NotRequired[Union[str, dict[str, str]]]

    data_json: NotRequired[str]
    table_html: NotRequired[str]
    table_style: NotRequired[str]

    selected_rows: NotRequired[Sequence[int]]
    filtered_row_count: NotRequired[int]

    downsampling_warning: NotRequired[str]
    text_in_header_can_be_selected: NotRequired[bool]

    column_filters: NotRequired[Literal[False, "header", "footer"]]
    keys_to_be_evaluated: NotRequired[Sequence[Sequence[Union[int, str]]]]

    # These options are used in the HTML template
    # and don't reach the PyDataTablesRenderer JavaScript class
    connected: NotRequired[bool]
    dt_url: NotRequired[str]
    display_logo_when_loading: NotRequired[bool]


_OPTIONS_MODULE = "pydatatables.options"


def get_silence_msg(option_name: str) -> str:
    return _get_silence_msg(option_name, _OPTIONS_MODULE)


def check_itable_arguments(kwargs: "dict[str, Any]", typed_dict: type) -> None:
    """
    Check the arguments passed to the PyDataTablesRenderer constructor
    """
    warn_on_undocumented_option = (
        kwargs.get if typed_dict is PyDataTablesOptions else kwargs.pop
    )("warn_on_undocumented_option", False)

    warn_on_unexpected_option_type = (
        kwargs.get if typed_dict is PyDataTablesOptions else kwargs.pop
    )("warn_on_unexpected_option_type", False)

    if warn_on_undocumented_option:
        check_itable_argument_names(set(kwargs), typed_dict)

    if warn_on_unexpected_option_type:
        check_itable_argument_types(kwargs, typed_dict)


def check_itable_argument_names(names: "set[str]", typed_dict: type) -> None:
    """
    Check that the arguments passed to the PyDataTablesRenderer constructor
    are documented in the given TypedDict.
    """
    check_documented_option_names(names, typed_dict, _OPTIONS_MODULE)


def check_itable_argument_types(kwargs: "dict[str, Any]", typed_dict: type) -> None:
    """
    Check that the argments passed to the PyDataTablesRenderer constructor
    match the types defined in the given TypedDict.
    """
    check_documented_option_types(kwargs, typed_dict, _OPTIONS_MODULE)
