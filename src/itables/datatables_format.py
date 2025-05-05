import json
import warnings

import numpy as np
import pandas as pd
import pandas.io.formats.format as fmt

try:
    import polars as pl
except ImportError:
    pl = None


def _format_column(x, pure_json=False):
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
        if pure_json:
            # While JavaScript accept these values,
            # JSON (in the streamlit component)
            # cannot encode non-finite float values
            x = [f if np.isfinite(f) else str(f) for f in x]

    return x


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


def datatables_rows(df, count=None, warn_on_unexpected_types=False, pure_json=False):
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
        data = list(
            zip(
                *(empty_columns + [_format_column(x, pure_json) for _, x in df.items()])
            )
        )
        return json.dumps(
            data,
            cls=generate_encoder(warn_on_unexpected_types),
            allow_nan=not pure_json,
        )
    except AttributeError:
        # Polars DataFrame
        data = df.rows()

        return json.dumps(data, cls=generate_encoder(False), allow_nan=not pure_json)
