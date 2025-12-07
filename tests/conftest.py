import itertools as it

import pytest

import itables

try:
    dict_of_test_pandas_dfs = itables.sample_pandas_dfs.get_dict_of_test_dfs()
except AttributeError:
    dict_of_test_pandas_dfs = {}

try:
    dict_of_test_polars_dfs = itables.sample_polars_dfs.get_dict_of_test_dfs()
except AttributeError:
    dict_of_test_polars_dfs = {}


@pytest.fixture(params=list(dict_of_test_pandas_dfs.keys()))
def pd_df(request):
    name = request.param
    df = dict_of_test_pandas_dfs[name]
    return df


@pytest.fixture(params=list(dict_of_test_polars_dfs.keys()))
def pl_df(request):
    name = request.param
    df = dict_of_test_polars_dfs[name]
    return df


@pytest.fixture(
    params=[
        f"{name}_{lib}"
        for lib, name in list(it.product(["pd"], dict_of_test_pandas_dfs.keys()))
        + list(it.product(["pl"], dict_of_test_polars_dfs.keys()))
    ]
)
def df(request):
    name, lib = request.param.rsplit("_", 1)
    if lib == "pd":
        return dict_of_test_pandas_dfs[name]
    else:
        return dict_of_test_polars_dfs[name]


@pytest.fixture(params=["None", "1D-array", "2D-array"])
def lengthMenu(request):
    if request.param == "1D-array":
        return [2, 5, 10, 20, 50]
    if request.param == "2D-array":
        return [[10, 25, 50, 100, -1], [10, 25, 50, 100, "All"]]
    return None


@pytest.fixture(params=[False, True])
def connected(request):
    return request.param


@pytest.fixture(params=[False, True])
def use_to_html(request):
    return request.param


@pytest.fixture(autouse=True)
def no_itables_config_env_variable(monkeypatch):
    monkeypatch.delenv("ITABLES_CONFIG", raising=False)
    yield
    monkeypatch.undo()
