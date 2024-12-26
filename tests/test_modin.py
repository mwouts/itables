import pytest

from itables import to_html_datatable
from itables.sample_dfs import get_dict_of_test_modin_dfs, get_dict_of_test_modin_series

pytest.importorskip("modin")


@pytest.fixture(params=get_dict_of_test_modin_dfs().items(), ids=lambda param: param[0])
def df(request):
    return request.param[1]


@pytest.fixture(
    params=get_dict_of_test_modin_series().items(), ids=lambda param: param[0]
)
def x(request):
    return request.param[1]


def test_show_modin_series(x, use_to_html):
    to_html_datatable(x, use_to_html)


def test_show_modin_df(df, use_to_html):
    to_html_datatable(df, use_to_html)
