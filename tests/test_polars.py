import pytest

from itables import to_html_datatable
from itables.javascript import datatables_rows
from itables.sample_dfs import get_dict_of_test_dfs, get_dict_of_test_series

try:
    import polars  # noqa
except ImportError as e:
    pytest.skip(str(e), allow_module_level=True)


@pytest.mark.parametrize(
    "name,x", [(name, x) for name, x in get_dict_of_test_series(polars=True).items()]
)
def test_show_polars_series(name, x, use_to_html):
    to_html_datatable(x, use_to_html)


@pytest.mark.parametrize(
    "name,df", [(name, df) for name, df in get_dict_of_test_dfs(polars=True).items()]
)
def test_show_polars_df(name, df, use_to_html):
    to_html_datatable(df, use_to_html)


def test_encode_mixed_contents():
    # Make sure that the bigint escape works for mixed content # 291
    df = polars.DataFrame(
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


def test_value_counts_shown_as_string():
    """
    We don't want to pass dicts to datatable
    as these appear as 'Object', cf. #290
    """
    count = polars.DataFrame(["id_1"], schema={"col_1"}).select(
        polars.col("col_1").value_counts()
    )
    assert datatables_rows(count) == [
        ["{'col_1': 'id_1', 'count': 1}"]
    ]  # e.g. a str, not a dict
