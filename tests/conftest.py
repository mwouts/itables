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


@pytest.fixture(params=[False, True])
def connected(request):
    return request.param


@pytest.fixture(params=[False, True])
def use_to_html(request):
    try:
        import pandas as pd
    except ImportError:
        pytest.skip("Pandas is not available")
    if int((pd.__version__).split(".", 1)[0]) <1 and request.param:
        pytest.skip("Pandas.to_html is not available in Pandas < 1.0")

    return request.param


@pytest.fixture(autouse=True)
def no_itables_config_env_variable(monkeypatch):
    monkeypatch.delenv("ITABLES_CONFIG", raising=False)
    yield
    monkeypatch.undo()
