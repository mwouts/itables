import pandas as pd
import pytest

from itables import show
from itables.sample_dfs import (
    get_countries,
    get_dict_of_test_dfs,
    get_dict_of_test_series,
    get_indicators,
    get_population,
)


def test_get_countries():
    df = get_countries()
    assert len(df.columns) > 5
    assert len(df.index) > 100
    show(df)


def test_get_population():
    x = get_population()
    assert len(x) > 30
    assert x.max() > 7e9
    show(x)


def test_get_indicators():
    df = get_indicators()
    assert len(df.index) == 500
    assert len(df.columns)
    show(df)


@pytest.mark.parametrize("df_name,df", get_dict_of_test_dfs().items())
def test_show_test_dfs(df_name, df):
    show(df)


@pytest.mark.parametrize("series_name,series", get_dict_of_test_series().items())
def test_show_test_series(series_name, series):
    show(series)


def test_show_df_with_duplicate_column_names():
    df = pd.DataFrame({"a": [0], "b": [0.0], "c": ["str"]})
    df.columns = ["duplicated_name"] * 3
    show(df)
