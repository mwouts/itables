import contextlib
import json
import warnings

import numpy as np
import pandas as pd
import pandas.io.formats.format as fmt

import itables.options as opt


def _format_column(x):
    dtype_kind = x.dtype.kind
    if dtype_kind in ["b", "i", "s"]:
        return x

    # If pandas version >= 0.25.0 use the new method format_array with parameter 'leading_space'
    if pd.__version__ >= "0.25.0":
        x = fmt.format_array(x._values, None, justify="all", leading_space=False)
    else:
        # If pandas version < 0.25.0 use the old method format_array with parameter 'leading_space'
        x = fmt.format_array(x._values, None, justify="all")
    if dtype_kind == "f":
        with contextlib.suppress(ValueError):
            return np.array(x).astype(float)
    return x


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
        with contextlib.suppress(AttributeError):
            if obj is pd.NA:
                return str(obj)
        if opt.warn_on_unexpected_types:
            warnings.warn(
                "Unexpected type '{}' for '{}'.\n"
                "You can report this warning at https://github.com/mwouts/itables/issues\n"
                "To ignore the warning, please run:\n"
                "    import itables.options as opt\n"
                "    opt.warn_on_unexpected_types = False".format(type(obj), obj),
                category=RuntimeWarning,
            )
        return str(obj)


def datatables_rows(df):
    """Format the values in the table and return the data, row by row, as requested by DataTables"""
    # We iterate over columns using an index rather than the column name
    # to avoid an issue in case of duplicated column names #89
    data = list(zip(*(_format_column(x) for _, x in df.items())))
    return json.dumps(data, cls=TableValuesEncoder)
