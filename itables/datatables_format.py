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


def datatables_rows(df, count=None):
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

    data = list(zip(*(empty_columns + [_format_column(x) for _, x in df.items()])))
    return json.dumps(data, cls=TableValuesEncoder)
