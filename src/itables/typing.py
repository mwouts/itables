import re
import sys
import warnings
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from typing import Any, Literal, Mapping, Optional, Sequence, TypedDict, Union

# Conditional imports based on Python version
if sys.version_info >= (3, 11):
    from typing import NotRequired, TypeAlias, Unpack
else:
    try:
        from typing_extensions import NotRequired, TypeAlias, Unpack
    except ImportError:
        # Fallback for when typing_extensions is not available
        NotRequired = Any  # type: ignore
        TypeAlias = Any  # type: ignore
        Unpack = Any  # type: ignore

if sys.version_info >= (3, 10):
    pass  # TypeAlias already imported above
elif sys.version_info < (3, 11):
    try:
        from typing_extensions import TypeAlias
    except ImportError:
        TypeAlias = Any  # type: ignore

__all__ = [
    "NotRequired",
    "TypeAlias",
    "Unpack",
    "DataFrameModuleName",
    "DataFrameTypeName",
    "DataFrameOrSeries",
]

DataFrameModuleName: TypeAlias = Optional[str]
DataFrameTypeName: TypeAlias = Optional[str]

"""
A Pandas or Polars DataFrame or Series, a numpy array, or a Pandas Style object.
"""
DataFrameOrSeries: TypeAlias = Any


def get_dataframe_type_description(df: DataFrameOrSeries) -> str:
    """
    Return a string description of the type of the given DataFrame or Series.
    """
    if df is None:
        return "None"
    module = type(df).__module__
    if module.startswith("modin.pandas."):
        return f"modin.pandas.{type(df).__name__}"
    if module.startswith("narwhals."):
        return f"{get_dataframe_type_description(df.to_native())} (narwhalified)"
    return f"{type(df).__module__.split('.', 1)[0]}.{type(df).__name__}"


def get_dataframe_module_and_type_name(
    df: DataFrameOrSeries,
) -> tuple[DataFrameModuleName, DataFrameTypeName]:
    """
    Return the module and type name of the given DataFrame or Series.
    """
    if df is None:
        return None, None
    return type(df).__module__.split(".", 1)[0], type(df).__name__


def get_dataframe_module_name(df: DataFrameOrSeries) -> DataFrameModuleName:
    """
    Return the module name of the given DataFrame or Series.
    """
    if df is None:
        return None
    return type(df).__module__.split(".", 1)[0]


class JavascriptFunction(str):
    """
    A class that explicitly states that a string is
    a Javascript function. It will be converted to a
    real Javascript function using indirect evaluation.

    Please use this only for code that you trust.
    """

    def __init__(self, value: str):
        assert re.compile(r"^\s*function\s*\(").match(
            value
        ), "A Javascript function is expected to start with 'function('"


class JavascriptCode(str):
    """
    A class that explicitly states that a string is
    a Javascript code snippet. It will be converted to
    real Javascript code using indirect evaluation.

    Please use this only for code that you trust.
    """

    pass


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

    # DataTable options provided by its extensions
    buttons: NotRequired[Sequence[Union[str, Mapping[str, Any]]]]
    columnControl: NotRequired[Any]
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

    table_id: NotRequired[str]
    dt_url: NotRequired[str]
    dt_bundle: NotRequired[Union[str, Path]]
    connected: NotRequired[bool]
    display_logo_when_loading: NotRequired[bool]

    footer: NotRequired[bool]

    warn_on_unexpected_types: NotRequired[bool]
    warn_on_selected_rows_not_rendered: NotRequired[bool]
    warn_on_undocumented_option: NotRequired[bool]
    warn_on_unexpected_option_type: NotRequired[bool]
    text_in_header_can_be_selected: NotRequired[bool]

    column_filters: NotRequired[Literal[False, "header", "footer"]]

    use_to_html: NotRequired[bool]


class DTForITablesOptions(DataTableOptions):
    """
    The options that can be passed to the ITable constructor
    in the dt_for_itables package.
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
    # and don't reach the ITable JavaScript class
    connected: NotRequired[bool]
    dt_url: NotRequired[str]
    display_logo_when_loading: NotRequired[bool]


def is_typeguard_available() -> bool:
    """Check if typeguard is available"""
    try:
        typeguard_version = version("typeguard")
    except PackageNotFoundError:
        return False
    else:
        major, minor, bugfix = typeguard_version.split(".", 2)
        bugfix_int = int(
            re.match(
                r"(\d+)", bugfix
            ).group(  # pyright: ignore[reportOptionalMemberAccess]
                1
            )
        )
        return (int(major), int(minor), bugfix_int) >= (4, 4, 1)


def check_itable_arguments(kwargs: dict[str, Any], typed_dict: type) -> None:
    """
    Check the arguments passed to the ITable constructor
    """
    warn_on_undocumented_option = (
        kwargs.get if typed_dict is ITableOptions else kwargs.pop
    )("warn_on_undocumented_option", False)

    warn_on_unexpected_option_type = (
        kwargs.get if typed_dict is ITableOptions else kwargs.pop
    )("warn_on_unexpected_option_type", False)

    if warn_on_undocumented_option:
        check_itable_argument_names(set(kwargs), typed_dict)

    if warn_on_unexpected_option_type:
        check_itable_argument_types(kwargs, typed_dict)


def get_silence_msg(option_name: str) -> str:
    return (
        "You can silence this warning by setting "
        f"`itables.options.{option_name}=False`. If you believe ITableOptions "
        "should be updated, please make a PR or open an issue at https://github.com/mwouts/itables"
    )


def check_itable_argument_names(names: set[str], typed_dict: type) -> None:
    """
    Check that the arguments passed to the ITable constructor
    are documented in the given TypedDict.
    """
    documented_options = set(typed_dict.__required_keys__).union(
        typed_dict.__optional_keys__
    )
    undocumented_options = names - documented_options
    if undocumented_options:
        warnings.warn(
            f"These arguments are not documented in {typed_dict.__name__}: {undocumented_options}. "
            + get_silence_msg("warn_on_undocumented_option"),
            category=SyntaxWarning,
        )


def check_itable_argument_types(kwargs: dict[str, Any], typed_dict: type) -> None:
    """
    Check that the argments passed to the ITable constructor
    match the types defined in the given TypedDict.
    """
    try:
        from typeguard import TypeCheckError, check_type
    except ImportError as e:
        raise ImportError(
            "The `warn_on_unexpected_option_type` option requires the 'typeguard' package. "
            "Please install it using 'pip install typeguard', "
            "or deactivate the check by setting `itables.options.warn_on_unexpected_option_type=False`."
        ) from e

    for key, value in kwargs.items():
        # Undocumented options are addressed through warn_on_undocumented_option
        if key not in typed_dict.__annotations__:
            continue

        try:
            check_type({key: value}, typed_dict)
        except TypeCheckError as e:
            type_repr = str(typed_dict.__annotations__[key]).replace("typing.", "")
            warnings.warn(
                f"{key}={value} does not match {type_repr}: {e}. "
                + get_silence_msg("warn_on_unexpected_option_type"),
                category=SyntaxWarning,
            )
