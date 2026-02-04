import json
import math
import os
import sys
import warnings
from typing import Any, Optional, Sequence

from .typing import DataFrameOrSeries, get_dataframe_module_name


def _format_pandas_series(
    x, escape_html: bool, format_floats_in_python: bool
) -> Sequence[Any]:
    dtype_kind = x.dtype.kind
    if dtype_kind in ["b", "i"]:
        return x

    if dtype_kind == "f" and not format_floats_in_python:
        # Return floats as-is
        return [escape_non_finite_float(v) for v in x._values]

    if dtype_kind == "s":
        if escape_html:
            return x
        return [escape_html_chars(i) for i in x]

    import pandas.io.formats.format as fmt

    try:
        formatted = fmt.format_array(x._values, None, justify="all", leading_space=False)  # type: ignore
    except TypeError:
        # Older versions of Pandas don't have 'leading_space'
        formatted = fmt.format_array(x._values, None, justify="all")  # type: ignore

    if escape_html:
        formatted = [escape_html_chars(i) for i in formatted]

    if dtype_kind == "f":
        return [
            {"display": formatted_value, "sort": rank}
            for formatted_value, rank in zip(
                formatted, x.rank(method="dense", na_option="bottom").astype(int)
            )
        ]

    return formatted


def _format_polars_series(
    x,
    escape_html: bool,
    format_floats_in_python: bool,
    warn_on_polars_get_fmt_not_found: bool,
) -> Sequence[Any]:
    """Format a Polars Series for DataTables display"""
    pl = sys.modules["polars"]
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

    if dtype.is_float() and not format_floats_in_python:
        return [escape_non_finite_float(v) for v in x.to_list()]

    if dtype == pl.String:
        formatted = x.to_list()
    elif dtype == pl.Enum or dtype == pl.Categorical:
        formatted = x.cast(pl.String).to_list()
    else:
        # Other types - use Polars' native formatting
        str_len_limit = int(os.environ.get("POLARS_FMT_STR_LEN", default=30))
        try:
            formatted = [x._s.get_fmt(i, str_len_limit) for i in range(len(x))]
        except AttributeError:
            if warn_on_polars_get_fmt_not_found:
                warnings.warn(
                    "Polars private formatting method '_s.get_fmt' not found. We will use str() instead. "
                    "Please report this warning at https://github.com/mwouts/itables/issues/484. "
                    "To silence this warning, please set warn_on_polars_get_fmt_not_found to False.\n"
                )
            formatted = [str(v) for v in x]

    if escape_html:
        formatted = [escape_html_chars(i) for i in formatted]

    if dtype.is_float():
        return [
            (
                {"display": None, "sort": 0}
                if rank is None
                else {
                    "display": formatted_value,
                    "sort": rank,
                }
            )
            for formatted_value, rank in zip(formatted, x.rank(method="dense"))
        ]

    return formatted


def _format_narwhals_series(
    x, escape_html: bool, format_floats_in_python: bool
) -> Sequence[Any]:
    """Format a Narwhals Series for DataTables display"""
    nw = sys.modules["narwhals"]
    dtype = x.dtype

    # Boolean and integer types - return as-is
    if dtype in (
        nw.Boolean,
        nw.Int8,
        nw.Int16,
        nw.Int32,
        nw.Int64,
        nw.UInt8,
        nw.UInt16,
        nw.UInt32,
        nw.UInt64,
    ):
        return [v for v in x]

    # Float types - format and handle non-finite values
    if dtype.is_float() and not format_floats_in_python:
        return [escape_non_finite_float(v) for v in x]

    formatted = [str(v) for v in x]
    if escape_html:
        formatted = [escape_html_chars(i) for i in formatted]

    if dtype.is_float():
        return [
            {
                "display": formatted_value,
                "sort": int(rank) if rank is not None else 0,
            }
            for formatted_value, rank in zip(formatted, x.rank(method="dense"))
        ]

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
    if isinstance(value, str):
        return value.replace("&", r"&amp;").replace("<", r"&lt;").replace(">", r"&gt;")
    return value


def generate_encoder(warn_on_unexpected_types: bool = True) -> Any:
    """Generate a JSON encoder that can handle special types like numpy"""

    class TableValuesEncoder(json.JSONEncoder):
        def default(self, o):
            if isinstance(o, (bool, int, float, str)):
                return json.JSONEncoder.default(self, o)
            module = type(o).__module__
            if module == "numpy":
                import numpy as np

                if isinstance(o, np.bool_):
                    return bool(o)
                if isinstance(o, np.integer):
                    return int(o)
                if isinstance(o, np.floating):
                    return float(o)
            pd = sys.modules.get("pandas", None)
            if pd is not None and o is pd.NA:
                return str(o)

            if warn_on_unexpected_types:
                warnings.warn(
                    f"Unexpected type '{type(o)}' for '{o}'.\n"
                    "You can report this warning at https://github.com/mwouts/itables/issues\n"
                    "To silence this warning, please run:\n"
                    "    itables.options.warn_on_unexpected_types = False",
                    category=RuntimeWarning,
                )
            return str(o)

    return TableValuesEncoder


def datatables_rows(
    df: DataFrameOrSeries,
    *,
    column_count: Optional[int] = None,
    escape_html: bool = True,
    float_columns_to_be_formatted_in_python: Optional[set[int]] = None,
    warn_on_unexpected_types: bool = False,
    warn_on_polars_get_fmt_not_found: bool = True,
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

    df_module = get_dataframe_module_name(df)
    if float_columns_to_be_formatted_in_python is None:
        float_columns_to_be_formatted_in_python = set()
    if df_module == "pandas":
        formatted_columns = [
            _format_pandas_series(
                x, escape_html, i in float_columns_to_be_formatted_in_python
            )
            for i, (_, x) in enumerate(df.items())
        ]
    elif df_module == "polars":
        formatted_columns = [
            _format_polars_series(
                df[col],
                escape_html,
                i in float_columns_to_be_formatted_in_python,
                warn_on_polars_get_fmt_not_found,
            )
            for i, col in enumerate(df.columns)
        ]
    else:
        # Other DataFrame types are handled via Narwhals, and are expected
        # to have been converted to Narwhals already (except in tests)
        import narwhals as nw

        df = nw.from_native(df, eager_only=True, allow_series=True)

        formatted_columns = [
            _format_narwhals_series(
                df[col], escape_html, i in float_columns_to_be_formatted_in_python
            )
            for i, col in enumerate(df.columns)
        ]

    data = list(zip(*(empty_columns + formatted_columns)))

    return json.dumps(
        data,
        cls=generate_encoder(warn_on_unexpected_types),
        allow_nan=False,
    )
