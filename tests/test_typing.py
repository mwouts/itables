import re

import pytest

import itables

if not itables.typing.is_typeguard_available():
    pytestmark = pytest.mark.skip(reason="Typeguard is not available")


@pytest.fixture
def df():
    return itables.sample_dfs.get_countries(html=False)


def test_warns_on_incorrect_option(df):
    with pytest.warns(
        SyntaxWarning,
        match="These arguments are not documented in ITableOptions: .*'lengthMenuWithTypo'",
    ):
        itables.to_html_datatable(df, lengthMenuWithTypo=[2, 5, 10])  # type: ignore


def test_warns_on_incorrect_type(df):
    with pytest.warns(SyntaxWarning, match=re.escape("does not match")):
        itables.to_html_datatable(df, lengthMenu=[2.2])  # type: ignore
