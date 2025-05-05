import json
import warnings

import numpy as np
import pandas as pd
import pandas.io.formats.format as fmt

try:
    import polars as pl
except ImportError:
    pl = None


def _format_column(x):
    dtype_kind = x.dtype.kind
    if dtype_kind in ["b", "i", "s"]:
        return x

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


def datatables_rows(df, count=None, warn_on_unexpected_types=False):
    """Format the values in the table and return the data, row by row, as requested by DataTables"""
    # We iterate over columns using an index rather than the column name
    # to avoid an issue in case of duplicated column names #89
    if count is None or len(df.columns) == count:
        empty_columns = []
    else:
        # When the header requires more columns (#141), we append empty columns on the left
        missing_columns = count - len(df.columns)
        assert missing_columns > 0
        empty_columns = [[None] * len(df)] * missing_columns

    try:
        # Pandas DataFrame
        data = list(zip(*(empty_columns + [_format_column(x) for _, x in df.items()])))
        return json.dumps(
            data,
            cls=generate_encoder(warn_on_unexpected_types),
            allow_nan=False,
        )
    except AttributeError:
        # Polars DataFrame
        data = df.rows()
        data = [[escape_non_finite_float(f) for f in row] for row in data]

        return json.dumps(data, cls=generate_encoder(False), allow_nan=False)
