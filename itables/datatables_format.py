import json

import numpy as np
import pandas.io.formats.format as fmt


def _format_column(x):
    dtype_kind = x.dtype.kind
    if dtype_kind in ["b", "i", "s"]:
        return x

    if dtype_kind == "O":
        return x.astype(str)

    x = fmt.format_array(x.values, None)
    if dtype_kind == "f":
        try:
            return np.array(x).astype(float)
        except ValueError:
            pass
    if dtype_kind in ["m", "M"]:
        # NaT is padded with spaces
        return [s.lstrip() for s in x]

    return x


class TableValuesEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (bool, int, float, str)):
            return json.JSONEncoder.default(self)
        if isinstance(obj, np.bool_):
            return bool(obj)
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        return str(obj)


def datatables_rows(df):
    """Format the values in the table and return the data, row by row, as requested by DataTables"""
    # We iterate over columns using an index rather than the column name
    # to avoid an issue in case of duplicated column names #89
    data = list(zip(*(_format_column(x) for _, x in df.items())))
    return json.dumps(data, cls=TableValuesEncoder)
