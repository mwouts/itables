"""Typing helpers shared by the ITables packages (pydatatables, pyaggrid)"""

import re
import warnings
from importlib.metadata import PackageNotFoundError, version
from typing import (
    TYPE_CHECKING,
    Any,
    Optional,
)

try:
    from typing import TypeAlias  # py3.10+
except ImportError:
    try:
        from typing_extensions import TypeAlias  # type: ignore
    except ImportError:
        if TYPE_CHECKING:
            raise
        TypeAlias = Any  # type: ignore

try:
    from typing import NotRequired, Unpack  # py3.11+
except ImportError:
    try:
        from typing_extensions import NotRequired, Unpack  # type: ignore
    except ImportError:
        if TYPE_CHECKING:
            raise

        class _SubscriptableFallback:
            def __getitem__(self, item):
                return Any

        NotRequired = _SubscriptableFallback()  # type: ignore
        Unpack = _SubscriptableFallback()  # type: ignore

__all__ = [
    "NotRequired",
    "TypeAlias",
    "Unpack",
    "DataFrameModuleName",
    "DataFrameTypeName",
    "DataFrameOrSeries",
    "JavascriptCode",
    "JavascriptFunction",
    "get_dataframe_type_description",
    "get_dataframe_module_and_type_name",
    "get_dataframe_module_name",
    "is_typeguard_available",
    "check_documented_option_names",
    "check_documented_option_types",
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


def get_silence_msg(option_name: str, options_module: str) -> str:
    return (
        "You can silence this warning by setting "
        f"`{options_module}.{option_name}=False`. If you believe the documented options "
        "should be updated, please make a PR or open an issue at https://github.com/mwouts/itables"
    )


def check_documented_option_names(
    names: "set[str]", typed_dict: type, options_module: str
) -> None:
    """
    Check that the given option names are documented in the given TypedDict.
    """
    documented_options = set(typed_dict.__required_keys__).union(
        typed_dict.__optional_keys__
    )
    undocumented_options = names - documented_options
    if undocumented_options:
        warnings.warn(
            f"These arguments are not documented in {typed_dict.__name__}: {undocumented_options}. "
            + get_silence_msg("warn_on_undocumented_option", options_module),
            category=SyntaxWarning,
        )


def check_documented_option_types(
    kwargs: "dict[str, Any]", typed_dict: type, options_module: str
) -> None:
    """
    Check that the given options match the types defined in the given TypedDict.
    """
    try:
        from typeguard import TypeCheckError, check_type
    except ImportError as e:
        raise ImportError(
            "The `warn_on_unexpected_option_type` option requires the 'typeguard' package. "
            "Please install it using 'pip install typeguard', "
            f"or deactivate the check by setting `{options_module}.warn_on_unexpected_option_type=False`."
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
                + get_silence_msg("warn_on_unexpected_option_type", options_module),
                category=SyntaxWarning,
            )
