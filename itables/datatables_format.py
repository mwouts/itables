import json
import warnings

import numpy as np
import pandas as pd
import pandas.io.formats.format as fmt

try:
    import polars as pl
except ImportError:
    pl = None


JS_MAX_SAFE_INTEGER = 2**53 - 1
JS_MIN_SAFE_INTEGER = -(2**53 - 1)


def _format_column(x):
    dtype_kind = x.dtype.kind
    if dtype_kind in ["b", "i", "s"]:
        return x

    try:
        x = fmt.format_array(x._values, None, justify="all", leading_space=False)
    except TypeError:
        # Older versions of Pandas don't have 'leading_space'
        x = fmt.format_array(x._values, None, justify="all")
    if dtype_kind == "f":
        try:
            return np.array(x).astype(float)
        except ValueError:
            pass

    return x


def generate_encoder(warn_on_unexpected_types=True):
    class TableValuesEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, (bool, int, float, str)):
                return json.JSONEncoder.default(self, obj)
            if isinstance(obj, np.bool_):
                return bool(obj)
            if isinstance(obj, np.integer):
                return int(obj)
            if isinstance(obj, np.floating):
                return float(obj)
            try:
                if obj is pd.NA:
                    return str(obj)
            except AttributeError:
                pass

            if warn_on_unexpected_types:
                warnings.warn(
                    "Unexpected type '{}' for '{}'.\n"
                    "You can report this warning at https://github.com/mwouts/itables/issues\n"
                    "To silence this warning, please run:\n"
                    "    import itables.options as opt\n"
                    "    opt.warn_on_unexpected_types = False".format(type(obj), obj),
                    category=RuntimeWarning,
                )
            return str(obj)

    return TableValuesEncoder


def convert_bigints_to_str(df, warn_on_int_to_str_conversion):
    """In Javascript, integers have to remain between JS_MIN_SAFE_INTEGER and JS_MAX_SAFE_INTEGER."""
    converted = []
    for i, col in enumerate(df.columns):
        try:
            x = df.iloc[:, i]
            if (
                x.dtype.kind == "i"
                and (
                    ~x.isnull()
                    & ((x < JS_MIN_SAFE_INTEGER) | (x > JS_MAX_SAFE_INTEGER))
                ).any()
            ):
                df.iloc[:, i] = x.astype(str)
                converted.append(col)
        except AttributeError:
            # Polars
            x = df[col]
            if x.dtype in pl.INTEGER_DTYPES and (
                (x.min() < JS_MIN_SAFE_INTEGER) or (x.max() > JS_MAX_SAFE_INTEGER)
            ):
                df = df.with_columns(pl.col(col).cast(pl.Utf8))
                converted.append(col)

    if converted and warn_on_int_to_str_conversion:
        warnings.warn(
            "The columns {} contains integers that are too large for Javascript.\n"
            "They have been converted to str. See https://github.com/mwouts/itables/issues/172.\n"
            "To silence this warning, please run:\n"
            "    import itables.options as opt\n"
            "    opt.warn_on_int_to_str_conversion = False".format(converted)
        )

    return df


def datatables_rows(
    df, count=None, warn_on_unexpected_types=False, warn_on_int_to_str_conversion=False
):
    """Format the values in the table and return the data, row by row, as requested by DataTables"""
    df = convert_bigints_to_str(df, warn_on_int_to_str_conversion)

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
        return json.dumps(data, cls=generate_encoder(warn_on_unexpected_types))
    except AttributeError:
        # Polars DataFrame
        data = list(df.iter_rows())
        return json.dumps(data, cls=generate_encoder(False))
