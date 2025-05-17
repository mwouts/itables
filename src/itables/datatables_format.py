import json
import warnings
from typing import Optional

import numpy as np
import pandas as pd
import pandas.io.formats.format as fmt

try:
    import polars as pl
except ImportError:
    pl = None


def _format_column(x, escape_html: bool):
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

    if dtype_kind == "f":
        try:
            x = np.array(x).astype(float)
        except ValueError:
            pass

        x = [escape_non_finite_float(f) for f in x]

    if escape_html:
        return [escape_html_chars(i) for i in x]

    return x


def escape_non_finite_float(value):
    """Encode non-finite float values to strings that will be parsed by parseJSON"""
    if not isinstance(value, float):
        return value
    if np.isnan(value):
        return "___NaN___"
    if value == np.inf:
        return "___Infinity___"
    if value == -np.inf:
        return "___-Infinity___"
    return value


def escape_html_chars(value):
    """Escape HTML special characters"""
    if isinstance(value, str):
        from pandas.io.formats.printing import pprint_thing  # type: ignore

        return pprint_thing(
            value, escape_chars={"&": r"&amp;", "<": r"&lt;", ">": r"&gt;"}
        ).strip()
    return value


def generate_encoder(warn_on_unexpected_types=True):
    class TableValuesEncoder(json.JSONEncoder):
        def default(self, o):
            if isinstance(o, (bool, int, float, str)):
                return json.JSONEncoder.default(self, o)
            if isinstance(o, np.bool_):
                return bool(o)
            if isinstance(o, np.integer):
                return int(o)
            if isinstance(o, np.floating):
                return float(o)
            try:
                if o is pd.NA:
                    return str(o)
            except AttributeError:
                pass

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


def _isetitem(df, i, value):
    """Older versions of Pandas don't have df.isetitem"""
    try:
        df.isetitem(i, value)
    except AttributeError:
        df.iloc[:, i] = value


def datatables_rows(
    df,
    column_count: Optional[int] = None,
    warn_on_unexpected_types: bool = False,
    escape_html: bool = True,
):
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

    try:
        # Pandas DataFrame
        data = list(
            zip(
                *(
                    empty_columns
                    + [_format_column(x, escape_html) for _, x in df.items()]
                )
            )
        )
        return json.dumps(
            data,
            cls=generate_encoder(warn_on_unexpected_types),
            allow_nan=False,
        )
    except AttributeError:
        # Polars DataFrame
        assert pl is not None

        # Convert Polars Struct to string #290
        if any(isinstance(df[col].dtype, pl.Struct) for col in df.columns):
            columns = {col: df[col] for col in df.columns}
            for col in df.columns:
                if isinstance(df[col].dtype, pl.Struct):
                    try:
                        columns[col] = df[col].cast(str)
                    except pl.exceptions.InvalidOperationError:
                        columns[col] = [str(x) for x in df[col]]
            df = pl.DataFrame(columns)

        data = df.rows()
        data = [[escape_non_finite_float(f) for f in row] for row in data]

        if escape_html:
            data = [[escape_html_chars(i) for i in row] for row in data]

        return json.dumps(data, cls=generate_encoder(False), allow_nan=False)
