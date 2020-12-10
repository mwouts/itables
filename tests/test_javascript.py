import pandas as pd

from itables import javascript


def test_datatables_repr_max_columns_none():
    test_df = pd.DataFrame([1, 2])
    with pd.option_context("display.max_columns", None):
        html = javascript._datatables_repr_(test_df)
        assert html
