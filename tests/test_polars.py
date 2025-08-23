import pytest

from itables import to_html_datatable
from itables.javascript import datatables_rows, get_itable_arguments
from itables.sample_dfs import (
    get_dict_of_polars_test_dfs,
    get_dict_of_polars_test_series,
)

try:
    import polars as pl  # noqa
except ImportError as e:
    pytest.skip(str(e), allow_module_level=True)


@pytest.mark.parametrize(
    "name,x", [(name, x) for name, x in get_dict_of_polars_test_series().items()]
)
def test_show_polars_series(name, x):
    to_html_datatable(x)


@pytest.mark.parametrize(
    "name,df", [(name, df) for name, df in get_dict_of_polars_test_dfs().items()]
)
def test_show_polars_df(name, df):
    to_html_datatable(df)


def test_encode_mixed_contents():
    # Make sure that the bigint escape works for mixed content # 291
    df = pl.DataFrame(
        {
            "bigint": [1666767918216000000],
            "int": [1699300000000],
            "float": [0.9510565400123596],
            "neg": [-0.30901700258255005],
        }
    )
    assert (
        datatables_rows(df)
        == "[[1666767918216000000, 1699300000000, 0.9510565400123596, -0.30901700258255005]]"
    )


def test_render_polars_struct():
    df = pl.DataFrame(
        {
            "X": ["A", "A", "B", "C", "C", "C"],
        }
    )
    assert (
        datatables_rows(df.select(pl.col("X").value_counts(sort=True)))
        == '[["{\\"C\\",3}"], ["{\\"A\\",2}"], ["{\\"B\\",1}"]]'
    )


@pytest.mark.parametrize("show_index", ["auto", False, True])
def test_show_index_has_no_effect_on_polars_dataframes(show_index):
    df = pl.DataFrame(
        {
            "A": [1, 2, 3],
            "B": [4, 5, 6],
        }
    )
    itable_args = get_itable_arguments(df, showIndex=show_index)
    assert "data_json" in itable_args, set(itable_args)
    assert itable_args["data_json"] == "[[1, 4], [2, 5], [3, 6]]"
