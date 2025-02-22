import warnings

import pandas as pd
import pytest

from itables.downsample import downsample
from itables.shiny import DT


def test_select_on_downsampled_df():
    """
    When a DF of 17 rows is downsampled to 3 rows,
    we can only select rows 0, 1, 16
    """
    df = pd.DataFrame({"x": range(17)})
    dn, _ = downsample(df, max_rows=3)
    assert len(dn) == 3

    with warnings.catch_warnings():
        warnings.simplefilter("error")
        DT(df, maxRows=3, selected_rows=[0, 1, 16])

    for row in [-1, 17]:
        with pytest.raises(IndexError, match="Selected rows out of range"):
            DT(df, maxRows=3, selected_rows=[row])

    for row in [2, 15]:
        with pytest.warns(match="no row with index between 2 and 15 can be selected"):
            DT(df, maxRows=3, selected_rows=[row])
