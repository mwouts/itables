import re

import pandas as pd
import pytest

import itables


@pytest.fixture
def df():
    return pd.DataFrame(
        {
            "a": [1, 2],
        }
    )


def test_warns_on_incorrect_option(df):
    with pytest.warns(
        SyntaxWarning,
        match="These arguments are not documented in ITableOptions: .*'lengthMenuWithTypo'",
    ):
        itables.to_html_datatable(df, lengthMenuWithTypo=[2, 5, 10])  # type: ignore


def test_warns_on_incorrect_type(df):
    if not itables.typing.is_typeguard_available():
        pytest.skip(reason="Typeguard is not available")

    with pytest.warns(SyntaxWarning, match=re.escape("does not match")):
        itables.to_html_datatable(df, lengthMenu=[2.2])  # type: ignore
