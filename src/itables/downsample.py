import math
from typing import Union

from itables.typing import (
    DataFrameModuleName,
    DataFrameOrSeries,
    get_dataframe_module_name,
)


def nbytes(df: DataFrameOrSeries, df_module_name: DataFrameModuleName = None) -> int:
    """Return an estimate for number of bytes used by the dataframe"""
    if df_module_name is None:
        df_module_name = get_dataframe_module_name(df)
        assert df_module_name is not None

    if df_module_name in ["pandas", "numpy"]:
        return sum(x.values.nbytes for _, x in df.items())
    else:
        # Polars or Narwhalified DataFrame
        return df.estimated_size()


def as_nbytes(mem: Union[int, float, str]) -> int:
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


def downsample(
    df: DataFrameOrSeries,
    df_module_name: DataFrameModuleName = None,
    max_rows: int = 0,
    max_columns: int = 0,
    max_bytes: Union[int, str] = 0,
) -> tuple[DataFrameOrSeries, str]:
    """Return a subset of the dataframe that fits the limits"""
    if df_module_name is None:
        df_module_name = get_dataframe_module_name(df)

    org_rows, org_columns, org_bytes = (
        len(df),
        len(df.columns),
        nbytes(df, df_module_name),
    )
    max_bytes_numeric = as_nbytes(max_bytes)
    df = _downsample(
        df,
        df_module_name,
        max_rows=max_rows,
        max_columns=max_columns,
        max_bytes=max_bytes_numeric,
    )

    if len(df) < org_rows or len(df.columns) < org_columns:
        downsampled = '<a href="https://mwouts.github.io/itables/downsampling.html">downsampled</a>'
        reasons = []
        if org_rows > max_rows > 0:
            reasons.append("maxRows={}".format(max_rows))
        if org_columns > max_columns > 0:
            reasons.append("maxColumns={}".format(max_columns))
        if org_bytes > max_bytes_numeric > 0:
            reasons.append("maxBytes={}".format(max_bytes))

        if len(df.columns) < org_columns:
            downsampled_warning = f"{downsampled} from {org_rows:,d}x{org_columns:,d} to {len(df):,d}x{len(df.columns):,d} as {' and '.join(reasons)}"
        else:
            downsampled_warning = (
                f"{downsampled} from {org_rows:,d} rows as {' and '.join(reasons)}"
            )

        return df, downsampled_warning

    return df, ""


def shrink_towards_target_aspect_ratio(
    rows: int, columns: int, shrink_factor: float, target_aspect_ratio: float
) -> tuple[int, int]:
    """Return the number of rows and columns of the shrinked dataframe"""
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


def _downsample(
    df,
    df_module_name: DataFrameModuleName,
    max_rows=0,
    max_columns=0,
    max_bytes=0,
    target_aspect_ratio=None,
):
    """Implementation of downsample - may be called recursively"""
    if len(df) > max_rows > 0:
        second_half = max_rows // 2
        first_half = max_rows - second_half
        assert first_half >= second_half
        rows = list(range(first_half)) + list(range(len(df) - second_half, len(df)))
        if df_module_name == "pandas":
            df = df.iloc[rows]
        elif df_module_name == "polars":
            df = df[rows]
        else:
            raise TypeError(f"Unsupported DataFrame type: {df_module_name}")

    if len(df.columns) > max_columns > 0:
        second_half = max_columns // 2
        first_half = max_columns - second_half
        assert first_half >= second_half
        columns = list(range(first_half)) + list(
            range(len(df.columns) - second_half, len(df.columns))
        )
        if df_module_name == "pandas":
            df = df.iloc[:, columns]
        elif df_module_name == "polars":
            df = df[[df.columns[i] for i in columns]]
        else:
            raise TypeError(f"Unsupported DataFrame type: {df_module_name}")

    df_nbytes = nbytes(df, df_module_name)
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
                df,
                df_module_name,
                max_rows,
                max_columns,
                max_bytes,
                target_aspect_ratio,
            )

        # max_bytes is smaller than the average size of one cell
        # return a single cell with "..."
        return type(df)({df.columns[0]: ["..."]})

    return df
