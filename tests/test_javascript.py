import pandas as pd

from itables import javascript


def test_to_html_datatable_max_columns_none():
    test_df = pd.DataFrame([1, 2])
    with pd.option_context("display.max_columns", None):
        html = javascript.to_html_datatable(test_df)
        assert html
