import json
import re
import warnings
from typing import Any, Sequence

import numpy as np
import pandas as pd
import pandas.io.formats.format as fmt

from .typing import DataFrame

try:
    import polars as pl
except ImportError:
    pl = None


JS_MAX_SAFE_INTEGER = 2**53 - 1
JS_MIN_SAFE_INTEGER = -(2**53 - 1)


def _format_column(
    values: pd.Series, pure_json=False
) -> pd.Series | np.ndarray | Sequence[Any]:
    dtype_kind = values.dtype.kind
    if dtype_kind in ["b", "i", "s"]:
        return values

    x: pd.Series | np.ndarray | Sequence[Any]
    try:
        x = fmt.format_array(values._values, None, justify="all", leading_space=False)  # type: ignore
    except TypeError:
        # Older versions of Pandas don't have 'leading_space'
        x = fmt.format_array(values._values, None, justify="all")  # type: ignore

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


def generate_encoder(warn_on_unexpected_types: bool = True) -> Any:
    class TableValuesEncoder(json.JSONEncoder):
        def default(self, o: Any):
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
                    "Unexpected type '{}' for '{}'.\n"
                    "You can report this warning at https://github.com/mwouts/itables/issues\n"
                    "To silence this warning, please run:\n"
                    "    import itables.options as opt\n"
                    "    opt.warn_on_unexpected_types = False".format(type(o), o),
                    category=RuntimeWarning,
                )
            return str(o)

    return TableValuesEncoder


def _isetitem(df: pd.DataFrame, i: int, value: Any):
    """Older versions of Pandas don't have df.isetitem"""
    try:
        df.isetitem(i, value)
    except AttributeError:
        df.iloc[:, i] = value


def datatables_rows(
    df: DataFrame,
    count: int | None = None,
    warn_on_unexpected_types: bool = False,
    pure_json: bool = False,
) -> str:
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
        has_bigints = any(
            x.dtype.kind == "i"
            and ((x > JS_MAX_SAFE_INTEGER).any() or (x < JS_MIN_SAFE_INTEGER).any())
            for _, x in df.items()
        )
        js = json.dumps(
            data,
            cls=generate_encoder(warn_on_unexpected_types),
            allow_nan=not pure_json,
        )
    except AttributeError:
        # Polars DataFrame
        import polars as pl

        assert isinstance(df, pl.DataFrame)
        data = df.rows()

        has_bigints = any(
            (
                x.dtype == pl.Int64
                and ((x > JS_MAX_SAFE_INTEGER).any() or (x < JS_MIN_SAFE_INTEGER).any())
            )
            or (x.dtype == pl.UInt64 and (x > JS_MAX_SAFE_INTEGER).any())
            for x in (df[col] for col in df.columns)
        )
        js = json.dumps(data, cls=generate_encoder(False), allow_nan=not pure_json)

    if has_bigints:
        js = n_suffix_for_bigints(js, pure_json=pure_json)

    return js


def n_suffix_for_bigints(js: str, pure_json: bool = False) -> str:
    def n_suffix(matchobj):
        if pure_json:
            return matchobj.group(1) + '"' + matchobj.group(2) + '"' + matchobj.group(3)
        return (
            matchobj.group(1)
            + 'BigInt("'
            + matchobj.group(2)
            + '")'
            + matchobj.group(3)
        )

    big_int_re = re.compile(r"^([\[\s]+)(-?\d{16,})(\]*)$")
    parts = js.split(",")
    return ",".join(re.sub(big_int_re, n_suffix, part) for part in parts)
