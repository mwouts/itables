import pytest

from itables import to_html_datatable
from itables.javascript import datatables_rows
from itables.sample_dfs import get_dict_of_test_ibis_dfs, get_dict_of_test_ibis_series

ibis = pytest.importorskip("ibis")


@pytest.fixture(params=get_dict_of_test_ibis_dfs().items(), ids=lambda param: param[0])
def df(request):
    return request.param[1]


@pytest.fixture(
    params=get_dict_of_test_ibis_series().items(), ids=lambda param: param[0]
)
def x(request):
    return request.param[1]


def test_show_ibis_series(x, use_to_html):
    to_html_datatable(x, use_to_html)


def test_show_ibis_df(df, use_to_html):
    to_html_datatable(df, use_to_html)


def test_encode_mixed_contents():
    # Make sure that the bigint escape works for mixed content # 291
    df = ibis.DataFrame(
        {
            "bigint": [1666767918216000000],
            "int": [1699300000000],
            "float": [0.9510565400123596],
            "neg": [-0.30901700258255005],
        }
    )
    assert (
        datatables_rows(df)
        == '[[BigInt("1666767918216000000"), 1699300000000, 0.9510565400123596, -0.30901700258255005]]'
    )
