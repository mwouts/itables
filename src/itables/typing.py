import warnings
from typing import Any, Literal, Mapping, TypedDict, Union

from typing_extensions import NotRequired


class JavascriptFunction(str):
    """A class that explicitly states that a string is a Javascript function"""

    def __init__(self, value):
        assert value.lstrip().startswith(
            "function"
        ), "A Javascript function is expected to start with 'function'"


class JavascriptCode(str):
    """A class that explicitly states that a string is a Javascript code"""

    pass


class DataTableOptions(TypedDict):
    """
    This structure provides a non-exhaustive list of options that can be passed
    to the DataTable constructor. See https://datatables.net/reference/option/
    for the corresponding documentation.
    """

    # DataTable options
    caption: NotRequired[str]
    lengthMenu: NotRequired[
        Union[list[Union[int, str, Mapping[str, Any]]], list[list[Union[int, str]]]]
    ]
    order: NotRequired[
        Union[list[list[Union[int, str]]], Mapping[str, Union[int, str]]]
    ]
    layout: NotRequired[Mapping[str, Union[None, str, Mapping[str, Any]]]]
    columnDefs: NotRequired[list[Mapping[str, Any]]]
    paging: NotRequired[bool]
    autoWidth: NotRequired[bool]
    scrollX: NotRequired[bool]
    scrollY: NotRequired[str]
    scrollCollapse: NotRequired[bool]
    language: NotRequired[Mapping[str, str]]
    search: NotRequired[Mapping[str, Any]]
    searchCols: NotRequired[list[Any]]
    initComplete: NotRequired[JavascriptFunction]
    fnInfoCallback: NotRequired[JavascriptFunction]

    # DataTable options provided by its extensions
    buttons: NotRequired[list[Union[str, Mapping[str, Any]]]]
    fixedColumns: NotRequired[Mapping[Literal["left", "right"], int]]
    searchPanes: NotRequired[Mapping[str, Any]]
    searchBuilder: NotRequired[Mapping[str, Any]]
    rowGroup: NotRequired[Mapping[str, Any]]
    select: NotRequired[Union[bool, str, Mapping[str, str]]]
    keys: NotRequired[bool]

    # Add addition of the dt_for_itables package
    filtered_row_count: NotRequired[int]


class ITableOptions(DataTableOptions):
    """
    A non-exhaustive list of options that can be passed
    to the ITable constructors
    """

    classes: NotRequired[str]
    style: NotRequired[str]

    showIndex: NotRequired[Union[bool, str]]

    maxBytes: NotRequired[Union[int, str]]
    maxRows: NotRequired[int]
    maxColumns: NotRequired[int]

    dt_url: NotRequired[str]
    dt_bundle: NotRequired[str]
    connected: NotRequired[bool]
    display_logo_when_loading: NotRequired[bool]

    column_filters: NotRequired[Literal[False, "header", "footer"]]
    footer: NotRequired[bool]

    selected_rows: NotRequired[list[int]]

    pre_dt_code: NotRequired[str]
    tags: NotRequired[str]

    warn_on_unexpected_types: NotRequired[bool]
    warn_on_dom: NotRequired[bool]
    warn_on_selected_rows_not_rendered: NotRequired[bool]
    warn_on_undocumented_option: NotRequired[bool]

    use_to_html: NotRequired[bool]
    eval_functions: NotRequired[bool]


def check_itable_arguments(kwargs: dict[str, Any], typed_dict: type) -> None:
    """
    Check the arguments passed to the ITable constructor
    """

    warn_on_undocumented_option = (
        kwargs.pop if typed_dict is DataTableOptions else kwargs.get
    )("warn_on_undocumented_option", False)
    if not warn_on_undocumented_option:
        return

    try:
        from typeguard import TypeCheckError, check_type
    except ImportError as e:
        raise ImportError(
            "The `warn_on_undocumented_option` option requires the 'typeguard' package. "
            "Please install it using 'pip install typeguard', "
            "or deactivate the check by setting `itables.options.warn_on_undocumented_option=False`."
        ) from e

    try:
        check_type(kwargs, typed_dict)
    except TypeCheckError as e:
        warnings.warn(
            f"These arguments are either not documented in ITableOptions, or don't have "
            f"the right type: {e}. You can silence this warning by setting "
            "`itables.options.warn_on_undocumented_option=False`. If you believe ITableOptions "
            " needs to be updated, please open an issue at https://github.com/mwouts/itables/issues.",
            category=RuntimeWarning,
        )
