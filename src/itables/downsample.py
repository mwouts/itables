import math

import pandas as pd


def nbytes(df):
    if isinstance(df, pd.DataFrame):
        return sum(x.values.nbytes for _, x in df.items())

    # Narwhals
    return df.estimated_size()


def as_nbytes(mem):
    if isinstance(mem, (int, float)):
        return int(mem)
    assert isinstance(mem, str), mem
    if mem.endswith("KB"):
        return int(float(mem[:-2]) * 2**10)
    if mem.endswith("MB"):
        return int(float(mem[:-2]) * 2**20)
    if mem.endswith("GB"):
        raise ValueError(
            f"You probably don't want to display "
            f"a table that large within an HTML page: {mem}"
        )
    if mem.endswith("B"):
        return int(float(mem[:-1]))
    return int(float(mem))


def downsample(df, max_rows=0, max_columns=0, max_bytes=0):
    """Return a subset of the dataframe that fits the limits"""
    org_rows, org_columns, org_bytes = len(df), len(df.columns), nbytes(df)
    max_bytes_numeric = as_nbytes(max_bytes)
    df = _downsample(
        df, max_rows=max_rows, max_columns=max_columns, max_bytes=max_bytes_numeric
    )

    if len(df) < org_rows or len(df.columns) < org_columns:
        link = '<a href="https://mwouts.github.io/itables/downsampling.html">downsampled</a>'
        reasons = []
        if org_rows > max_rows > 0:
            reasons.append("maxRows={}".format(max_rows))
        if org_columns > max_columns > 0:
            reasons.append("maxColumns={}".format(max_columns))
        if org_bytes > max_bytes_numeric > 0:
            reasons.append("maxBytes={}".format(max_bytes))

        warning = "{} from {:,d}x{:,d} to {:,d}x{:,d} as {}".format(
            link,
            org_rows,
            org_columns,
            len(df),
            len(df.columns),
            " and ".join(reasons),
        )

        return df, warning

    return df, ""


def shrink_towards_target_aspect_ratio(
    rows, columns, shrink_factor, target_aspect_ratio
):
    # current and target aspect ratio
    aspect_ratio = rows / float(columns)

    # Optimization problem:
    # row_shrink_factor * column_shrink_factor = shrink_factor
    # row_shrink_factor / column_shrink_factor * aspect_ratio = target_aspect_ratio (equal or closer to)
    # with 0 < row_shrink_factor, column_shrink_factor <= 1

    # row and column natural shrink factors
    row_shrink_factor = min(1, max(target_aspect_ratio / aspect_ratio, shrink_factor))
    column_shrink_factor = min(
        1, max(aspect_ratio / target_aspect_ratio, shrink_factor)
    )

    # and in case the above is not enough, we shrink in both directions
    common_shrink_factor = math.sqrt(
        shrink_factor / (row_shrink_factor * column_shrink_factor)
    )

    row_shrink_factor *= common_shrink_factor
    column_shrink_factor *= common_shrink_factor

    return int(rows * row_shrink_factor), int(columns * column_shrink_factor)


def _downsample(df, max_rows=0, max_columns=0, max_bytes=0, target_aspect_ratio=None):
    """Implementation of downsample - may be called recursively"""
    if len(df) > max_rows > 0:
        second_half = max_rows // 2
        first_half = max_rows - second_half
        if second_half:
            if isinstance(df, pd.DataFrame):
                df = pd.concat((df.iloc[:first_half], df.iloc[-second_half:]))
            else:
                from narwhals import concat

                df = concat([df.head(first_half), df.tail(second_half)], how="vertical")
        else:
            if isinstance(df, pd.DataFrame):
                df = df.iloc[:first_half]
            else:
                df = df.head(first_half)

    if len(df.columns) > max_columns > 0:
        second_half = max_columns // 2
        first_half = max_columns - second_half
        if second_half:
            if isinstance(df, pd.DataFrame):
                df = pd.concat(
                    (df.iloc[:, :first_half], df.iloc[:, -second_half:]), axis=1
                )
            else:
                first_and_last_columns = (
                    df.columns[:first_half] + df.columns[-second_half:]
                )
                df = df.select(first_and_last_columns)
        else:
            if isinstance(df, pd.DataFrame):
                df = df.iloc[:, :first_half]
            else:
                df = df.select(df.columns[:first_half])

    df_nbytes = nbytes(df)
    if df_nbytes > max_bytes > 0:
        if target_aspect_ratio is None:
            if max_rows > 0 and max_columns > 0:
                target_aspect_ratio = max_rows / float(max_columns)
            else:
                target_aspect_ratio = 1.0

        max_rows, max_columns = shrink_towards_target_aspect_ratio(
            len(df),
            len(df.columns),
            shrink_factor=max_bytes / float(df_nbytes),
            target_aspect_ratio=target_aspect_ratio,
        )

        if max_rows > 0 and max_columns > 0:
            return _downsample(
                df, max_rows, max_columns, max_bytes, target_aspect_ratio
            )

        # max_bytes is smaller than the average size of one cell
        return pd.DataFrame({df.columns[0]: ["..."]})

    return df