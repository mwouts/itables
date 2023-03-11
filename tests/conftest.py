import pandas as pd
import pytest

from itables.sample_dfs import get_dict_of_test_dfs


@pytest.fixture(params=list(get_dict_of_test_dfs()))
def df(request):
    name = request.param
    df = get_dict_of_test_dfs()[name]
    assert isinstance(df, pd.DataFrame)
    return df


@pytest.fixture(params=["None", "1D-array", "2D-array"])
def lengthMenu(request):
    if request.param == "1D-array":
        return [2, 5, 10, 20, 50]
    if request.param == "2D-array":
        return [[10, 25, 50, 100, -1], [10, 25, 50, 100, "All"]]
    return None


@pytest.fixture(params=["None", "lfrtip"])
def dom(request):
    if request.param == "None":
        return None
    return request.param
