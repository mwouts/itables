import warnings
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from typing import Any, Literal, Mapping, TypedDict, Union

from packaging.version import Version
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
    stateSave: NotRequired[bool]
    stateDuration: NotRequired[int]

    # DataTable options provided by its extensions
    buttons: NotRequired[list[Union[str, Mapping[str, Any]]]]
    fixedColumns: NotRequired[Mapping[Literal["left", "right", "start", "end"], int]]
    searchPanes: NotRequired[Mapping[str, Any]]
    searchBuilder: NotRequired[Mapping[str, Any]]
    rowGroup: NotRequired[Mapping[str, Any]]
    select: NotRequired[Union[bool, str, Mapping[str, str]]]
    keys: NotRequired[bool]


class ITableOptions(DataTableOptions):
    """
    A non-exhaustive list of options that can be passed
    to the show function and to the ITable Python classes.
    """

    classes: NotRequired[Union[str, list[str]]]
    style: NotRequired[Union[str, dict[str, str]]]
    selected_rows: NotRequired[list[int]]

    showIndex: NotRequired[Union[bool, str]]

    maxBytes: NotRequired[Union[int, str]]
    maxRows: NotRequired[int]
    maxColumns: NotRequired[int]

    allow_html: NotRequired[bool]

    table_id: NotRequired[str]
    dt_url: NotRequired[str]
    dt_bundle: NotRequired[Union[str, Path]]
    connected: NotRequired[bool]
    display_logo_when_loading: NotRequired[bool]

    footer: NotRequired[bool]

    warn_on_unexpected_types: NotRequired[bool]
    warn_on_selected_rows_not_rendered: NotRequired[bool]
    warn_on_undocumented_option: NotRequired[bool]
    text_in_header_can_be_selected: NotRequired[bool]

    column_filters: NotRequired[Literal[False, "header", "footer"]]

    use_to_html: NotRequired[bool]


class DTForITablesOptions(DataTableOptions):
    """
    The options that can be passed to the ITable constructor
    in the dt_for_itables package.
    """

    classes: NotRequired[Union[str, list[str]]]
    style: NotRequired[Union[str, dict[str, str]]]

    data_json: NotRequired[str]
    table_html: NotRequired[str]
    table_style: NotRequired[str]

    selected_rows: NotRequired[list[int]]
    filtered_row_count: NotRequired[int]

    downsampling_warning: NotRequired[str]
    text_in_header_can_be_selected: NotRequired[bool]

    column_filters: NotRequired[Literal[False, "header", "footer"]]
    keys_to_be_evaluated: NotRequired[list[list[Union[int, str]]]]

    # These options are used in the HTML template
    # and don't reach the ITable JavaScript class
    connected: NotRequired[bool]
    dt_url: NotRequired[str]
    display_logo_when_loading: NotRequired[bool]


def is_typeguard_available():
    """Check if typeguard is available"""
    try:
        typeguard_version = version("typeguard")
    except PackageNotFoundError:
        return False
    else:
        return Version(typeguard_version) >= Version("4.4.1")


def check_itable_arguments(kwargs: dict[str, Any], typed_dict: type) -> None:
    """
    Check the arguments passed to the ITable constructor
    """

    warn_on_undocumented_option = (
        kwargs.get if typed_dict is ITableOptions else kwargs.pop
    )("warn_on_undocumented_option", False)
    if not warn_on_undocumented_option:
        return

    silence_msg = (
        "You can silence this warning by setting "
        "`itables.options.warn_on_undocumented_option=False`. If you believe ITableOptions "
        "should be updated, please make a PR or open an issue at https://github.com/mwouts/itables"
    )

    documented_options = set(typed_dict.__required_keys__).union(
        typed_dict.__optional_keys__
    )
    undocumented_options = set(kwargs.keys()) - documented_options
    if undocumented_options:
        warnings.warn(
            f"These arguments are not documented in {typed_dict.__name__}: {undocumented_options}. "
            + silence_msg,
            category=SyntaxWarning,
        )

    try:
        from typeguard import TypeCheckError, check_type
    except ImportError as e:
        raise ImportError(
            "The `warn_on_undocumented_option` option requires the 'typeguard' package. "
            "Please install it using 'pip install typeguard', "
            "or deactivate the check by setting `itables.options.warn_on_undocumented_option=False`."
        ) from e

    for key, value in kwargs.items():
        if key in undocumented_options:
            continue
        try:
            check_type({key: value}, typed_dict)
        except TypeCheckError as e:
            type_repr = str(typed_dict.__annotations__[key]).replace("typing.", "")
            warnings.warn(
                f"{key}={value} does not match {type_repr}: {e}. " + silence_msg,
                category=SyntaxWarning,
            )
