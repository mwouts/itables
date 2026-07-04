"""DataFrame helpers shared by the ITables packages"""

from typing import Literal, Union

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
