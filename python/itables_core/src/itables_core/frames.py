"""DataFrame helpers shared by the ITables packages"""

import warnings
from typing import Literal, Optional, Sequence, Union

from .typing import DataFrameOrSeries, get_dataframe_module_and_type_name


def evaluate_show_index(
    df: DataFrameOrSeries, show_index: Union[bool, Literal["auto"]]
) -> bool:
    """
    We don't want to show trivial indices (RangeIndex with no name) on Pandas DataFrames.
    """
    if df is None:
        return False
    df_module_name, df_type_name = get_dataframe_module_and_type_name(df)
    if df_module_name != "pandas":
        return False
    if show_index != "auto":
        return show_index
    if df_type_name == "Styler":
        return evaluate_show_index(
            df.data,  # pyright: ignore[reportAttributeAccessIssue]
            show_index,
        )
    if df.index.name is not None:
        return True

    import pandas as pd

    return not isinstance(df.index, pd.RangeIndex)


def safe_reset_index(df):
    import pandas as pd

    assert isinstance(df, pd.DataFrame)
    try:
        return df.reset_index()
    except ValueError:
        # Issue #134: the above might fail if the index has duplicated names or if one of the
        # index names is already a column, with e.g "ValueError: cannot insert A, already exists"
        index_levels = [
            pd.Series(
                df.index.get_level_values(i),
                name=name
                or (
                    "index{}".format(i)
                    if isinstance(df.index, pd.MultiIndex)
                    else "index"
                ),
            )
            for i, name in enumerate(df.index.names)
        ]
        return pd.concat(index_levels + [df.reset_index(drop=True)], axis=1)


def warn_if_selected_rows_are_not_visible(
    selected_rows: Optional[Sequence[int]],
    full_row_count: int,
    data_row_count: int,
    warn_on_selected_rows_not_rendered: bool,
) -> Sequence[int]:
    """
    Issue a warning if the selected rows are not within the range of rendered rows.
    """
    if selected_rows is None:
        return []

    if not all(isinstance(i, int) for i in selected_rows):
        raise TypeError("Selected rows must be integers")

    if selected_rows and (
        min(selected_rows) < 0 or max(selected_rows) >= full_row_count
    ):
        raise IndexError("Selected rows out of range")

    if full_row_count == data_row_count:
        return selected_rows

    second_half = data_row_count // 2
    first_half = data_row_count - second_half
    assert first_half >= second_half

    bottom_limit = first_half
    top_limit = full_row_count - second_half

    if warn_on_selected_rows_not_rendered and any(
        bottom_limit <= i < top_limit for i in selected_rows
    ):
        not_shown = [i for i in selected_rows if bottom_limit <= i < top_limit]
        not_shown = ", ".join(
            [str(i) for i in not_shown[:6]] + (["..."] if len(not_shown) > 6 else [])
        )
        warnings.warn(
            f"This table has been downsampled, see https://mwouts.github.io/itables/downsampling.html. "
            f"Only {data_row_count} of the original {full_row_count} rows are rendered. "
            f"In particular these rows: [{not_shown}] cannot be selected "
            f"(more generally, no row with index between {bottom_limit} and {top_limit-1} "
            "can be selected). Hint: increase maxBytes if appropriate - see link above."
        )

    return [i for i in selected_rows if i < bottom_limit or i >= top_limit]
