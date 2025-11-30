import json
import math
import warnings
from typing import Any, Optional, Sequence, Union

from .typing import DataFrameOrSeries


def _format_pandas_series(
    x: "pd.Series[Any]", escape_html: bool
) -> "Union[pd.Series[Any],Sequence[Any]]":
    import pandas.io.formats.format as fmt

    dtype_kind = x.dtype.kind
    if dtype_kind in ["b", "i"]:
        return x

    if dtype_kind == "s":
        if escape_html:
            return x
        return [escape_html_chars(i) for i in x]

    try:
        x = fmt.format_array(x._values, None, justify="all", leading_space=False)  # type: ignore
    except TypeError:
        # Older versions of Pandas don't have 'leading_space'
        x = fmt.format_array(x._values, None, justify="all")  # type: ignore

    y: "Union[pd.Series[Any], Sequence[Any]]" = x
    if dtype_kind == "f":
        try:
            z = [float(i) for i in x]
        except ValueError:
            z = x
            pass

        y = [escape_non_finite_float(f) for f in z]

    if escape_html:
        return [escape_html_chars(i) for i in y]

    return y


def _format_polars_series(x: "pl.Series", escape_html: bool) -> Sequence[Any]:
    """Format a Polars Series for DataTables display"""
    import polars as pl  # noqa

    dtype = x.dtype

    # Boolean and integer types - return as-is
    if dtype in (
        pl.Boolean,
        pl.Int8,
        pl.Int16,
        pl.Int32,
        pl.Int64,
        pl.UInt8,
        pl.UInt16,
        pl.UInt32,
        pl.UInt64,
    ):
        return x.to_list()

    # String types - handle HTML escaping
    if dtype in (pl.Utf8, pl.String, pl.Categorical):
        values = x.to_list()
        if not escape_html:
            return [escape_html_chars(i) for i in values]
        return values

    # Float types - format and handle non-finite values
    if dtype in (pl.Float32, pl.Float64):
        # Format with Polars string conversion
        formatted = x.cast(str).to_list()

        # Convert back to float to handle NaN/Inf
        try:
            values = [
                escape_non_finite_float(float(v)) if v is not None else None
                for v in formatted
            ]
        except ValueError:
            values = formatted

        if escape_html:
            return [escape_html_chars(i) for i in values]
        return values

    # Date, datetime, duration types - convert to string
    if dtype in (pl.Date, pl.Datetime, pl.Time):
        formatted = x.cast(str).to_list()
        if escape_html:
            return [escape_html_chars(i) for i in formatted]
        return formatted

    if dtype == pl.Duration:
        # Convert to string by formatting the timedelta-like representation
        formatted = [str(v) if v is not None else None for v in x.to_list()]
        if escape_html:
            return [escape_html_chars(i) for i in formatted]
        return formatted

    # Struct types - convert to string representation
    if isinstance(dtype, pl.Struct):
        try:
            formatted = x.cast(str).to_list()
        except pl.exceptions.InvalidOperationError:
            formatted = [str(v) for v in x.to_list()]
        if escape_html:
            return [escape_html_chars(i) for i in formatted]
        return formatted

    # All other types - fallback to string conversion
    formatted = x.cast(str).to_list()
    if escape_html:
        return [escape_html_chars(i) for i in formatted]
    return formatted


def escape_non_finite_float(value: Any) -> Any:
    """Encode non-finite float values to strings that will be parsed by parseJSON"""
    if not isinstance(value, float):
        return value
    if math.isnan(value):
        return "___NaN___"
    if value == math.inf:
        return "___Infinity___"
    if value == -math.inf:
        return "___-Infinity___"
    return value


def escape_html_chars(value: Any) -> Any:
    """Escape HTML special characters"""
    if not isinstance(value, str):
        return value
    return value.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def generate_encoder(warn_on_unexpected_types: bool = True) -> Any:
    """Generate a JSON encoder that can handle special types like numpy"""

    class TableValuesEncoder(json.JSONEncoder):
        def default(self, o):
            if isinstance(o, (bool, int, float, str)):
                return json.JSONEncoder.default(self, o)

            type_module = type(o).__module__
            type_name = type(o).__name__

            if type_module == "numpy":
                if type_name.startswith("bool"):
                    return bool(o)
                if type_name.startswith(
                    "int"
                ):  # Matches int8, int16, int32, int64, etc.
                    return int(o)
                if type_name.startswith("float"):  # Matches float16, float32, float64
                    return float(o)

            if type_name == "NAType":
                return str(o)

            if warn_on_unexpected_types:
                warnings.warn(
                    f"Unexpected type '{type_module}.{type_name}' for '{o}'.\n"
                    "You can report this warning at https://github.com/mwouts/itables/issues\n"
                    "To silence this warning, please run:\n"
                    "    itables.options.warn_on_unexpected_types = False",
                    category=RuntimeWarning,
                )
            return str(o)

    return TableValuesEncoder


def datatables_rows(
    df: DataFrameOrSeries,
    column_count: Optional[int] = None,
    warn_on_unexpected_types: bool = False,
    escape_html: bool = True,
) -> str:
    """Format the values in the table and return the data, row by row, as requested by DataTables"""
    # We iterate over columns using an index rather than the column name
    # to avoid an issue in case of duplicated column names #89
    if column_count is None or len(df.columns) == column_count:
        empty_columns = []
    else:
        # When the header requires more columns (#141), we append empty columns on the left
        missing_columns = column_count - len(df.columns)
        assert missing_columns > 0
        empty_columns = [[None] * len(df)] * missing_columns

    df_module = type(df).__module__
    if df_module.startswith("pandas"):
        formatted_columns = [
            _format_pandas_series(x, escape_html) for _, x in df.items()
        ]
    elif df_module.startswith("polars"):
        formatted_columns = empty_columns + [
            _format_polars_series(df[col], escape_html) for col in df.columns
        ]
    else:
        raise TypeError(f"Unsupported DataFrame type: {df_module}")

    data = list(zip(*(empty_columns + formatted_columns)))

    return json.dumps(
        data,
        cls=generate_encoder(warn_on_unexpected_types),
        allow_nan=False,
    )
