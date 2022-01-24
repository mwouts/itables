import logging

import pandas as pd

logging.basicConfig()
logger = logging.getLogger(__name__)


def downsample(df, max_rows=0, max_columns=0, max_bytes=0):
    """Return a subset of the dataframe that fits the limits"""
    org_rows, org_columns, org_bytes = len(df.index), len(df.columns), df.values.nbytes
    df = _downsample(
        df, max_rows=max_rows, max_columns=max_columns, max_bytes=max_bytes
    )

    if len(df.index) < org_rows or len(df.columns) < org_columns:
        reasons = []
        if org_rows > max_rows > 0:
            reasons.append("maxRows={}".format(max_rows))
        if org_columns > max_columns > 0:
            reasons.append("maxColumns={}".format(max_columns))
        if org_bytes > max_bytes > 0:
            reasons.append("nbytes={}>{}=maxBytes".format(org_bytes, max_bytes))

        logger.warning(
            "showing {}x{} of {}x{} as {}. See https://mwouts.github.io/itables/downsampling.html".format(
                len(df.index),
                len(df.columns),
                org_rows,
                org_columns,
                " and ".join(reasons),
            )
        )

    return df


def _downsample(df, max_rows=0, max_columns=0, max_bytes=0):
    """Implementation of downsample - may be called recursively"""
    if len(df.index) > max_rows > 0:
        second_half = max_rows // 2
        first_half = max_rows - second_half
        if second_half:
            df = pd.concat((df.iloc[:first_half], df.iloc[-second_half:]))
        else:
            df = df.iloc[:first_half]

    if len(df.columns) > max_columns > 0:
        second_half = max_columns // 2
        first_half = max_columns - second_half
        if second_half:
            df = pd.concat((df.iloc[:, :first_half], df.iloc[:, -second_half:]), axis=1)
        else:
            df = df.iloc[:, :first_half]

    if df.values.nbytes > max_bytes > 0:
        max_rows = len(df.index)
        max_columns = len(df.columns)

        # we want to decrease max_rows * max_columns by df.values.nbytes / max_bytes
        max_product = max_rows * max_columns / (float(df.values.nbytes) / max_bytes)

        while max_product >= 1:
            max_rows = max(max_rows // 2, 1)
            if max_rows * max_columns <= max_product:
                return _downsample(df, max_rows, max_columns, max_bytes)

            max_columns = max(max_columns // 2, 1)
            if max_rows * max_columns <= max_product:
                return _downsample(df, max_rows, max_columns, max_bytes)

        # max_product < 1.0:
        df = df.iloc[:1, :1]
        df.iloc[0, 0] = "..."
        return df

    return df
