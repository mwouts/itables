import logging
import math

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
            reasons.append(f"maxRows={max_rows}")
        if org_columns > max_columns > 0:
            reasons.append(f"maxColumns={max_columns}")
        if org_bytes > max_bytes > 0:
            reasons.append(f"nbytes={org_bytes}>{max_bytes}=maxBytes")

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


def _downsample(df, max_rows=0, max_columns=0, max_bytes=0, target_aspect_ratio=None):
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
        # current and target aspect ratio
        aspect_ratio = len(df.index) / len(df.columns)
        if target_aspect_ratio is None:
            if max_rows > 0 and max_columns > 0:
                target_aspect_ratio = max_rows / max_columns
            else:
                target_aspect_ratio = 1.0

        # Optimization problem:
        # row_shrink_factor * column_shrink_factor = max_bytes / df.values.nbytes
        # row_shrink_factor / column_shrink_factor * aspect_ratio = target_aspect_ratio (equal or closer to)
        # with 0 < row_shrink_factor, column_shrink_factor <= 1

        # we need to decrease the area by this factor
        shrink_factor = max_bytes / df.values.nbytes

        # row and column natural shrink factors
        row_shrink_factor = min(
            1, max(target_aspect_ratio / aspect_ratio, shrink_factor)
        )
        column_shrink_factor = min(
            1, max(aspect_ratio / target_aspect_ratio, shrink_factor)
        )

        # and in case the above is not enough, we shrink in both directions
        common_shrink_factor = math.sqrt(
            shrink_factor / (row_shrink_factor * column_shrink_factor)
        )

        row_shrink_factor *= common_shrink_factor
        column_shrink_factor *= common_shrink_factor

        max_rows = int(len(df.index) * row_shrink_factor)
        max_columns = int(len(df.columns) * column_shrink_factor)

        if max_rows > 0 and max_columns > 0:
            return _downsample(
                df, max_rows, max_columns, max_bytes, target_aspect_ratio
            )

        # max_bytes is smaller than the average size of one cell
        df = df.iloc[:1, :1]
        df.iloc[0, 0] = "..."
        return df

    return df
