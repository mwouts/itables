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

    x = fmt.format_array(x.values, None, justify="all", leading_space=False)
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
                "Unexpected type {} for value {}. "
                "To ignore this warning, please set opt.warn_on_unexpected_types = False. "
                "You can also report this warning at https://github.com/mwouts/itables/issues".format(
                    type(obj), obj
                ),
                category=RuntimeWarning,
            )
        return str(obj)


def datatables_rows(df):
    """Format the values in the table and return the data, row by row, as requested by DataTables"""
    # We iterate over columns using an index rather than the column name
    # to avoid an issue in case of duplicated column names #89
    data = list(zip(*(_format_column(x) for _, x in df.items())))
    return json.dumps(data, cls=TableValuesEncoder)
