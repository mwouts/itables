import pandas as pd
import pytest

from itables.javascript import to_html_datatable


@pytest.fixture()
def df():
    return pd.DataFrame([1, 2])


def test_warn_on_unexpected_types_not_in_html(df):
    html = to_html_datatable(df)
    assert "warn_on_unexpected_types" not in html
