import json

import pytest

from itables import show, to_html_datatable
from itables.datatables_format import _format_polars_series, generate_encoder
from itables.javascript import datatables_rows, get_itable_arguments

try:
    import polars as pl
except ImportError:
    pytest.skip("Polars is not available", allow_module_level=True)
else:
    from itables.sample_polars_dfs import (
        get_countries,
        get_dict_of_test_dfs,
        get_dict_of_test_series,
        get_indicators,
        get_population,
    )

try:
    import IPython  # noqa F401
except ImportError:
    show = to_html_datatable


# Make sure that displaying a dataframe does not trigger a warning  #107
pytestmark = [
    pytest.mark.filterwarnings("error"),
]


@pytest.mark.parametrize(
    "name,x", [(name, x) for name, x in get_dict_of_test_series().items()]
)
def test_show_series(name, x):
    to_html_datatable(x)


@pytest.mark.parametrize(
    "name,df", [(name, df) for name, df in get_dict_of_test_dfs().items()]
)
def test_show_df(name, df):
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
    assert (
        datatables_rows(df, float_columns_to_be_formatted_in_python={2, 3})
        == "[[1666767918216000000, 1699300000000, "
        '{"display": "0.951057", "sort": 0.9510565400123596}, '
        '{"display": "-0.309017", "sort": -0.30901700258255005}]]'
    )


def test_render_struct():
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
def test_show_index_has_no_effect_on_dataframes(show_index):
    df = pl.DataFrame(
        {
            "A": [1, 2, 3],
            "B": [4, 5, 6],
        }
    )
    itable_args = get_itable_arguments(df, showIndex=show_index)
    assert "data_json" in itable_args, set(itable_args)
    assert itable_args["data_json"] == "[[1, 4], [2, 5], [3, 6]]"


def test_get_countries(connected):
    df = get_countries(html=True)
    assert len(df.columns) > 5
    assert len(df) > 100


def test_get_population(connected):
    x = get_population()
    assert len(x) > 30
    assert x.max() > 7e9  # type: ignore
    show(x, connected=connected)


def test_get_indicators(connected):
    df = get_indicators()
    assert len(df) == 500
    assert len(df.columns)
    show(df, connected=connected)


def kwargs_remove_none(**kwargs):
    return {key: value for key, value in kwargs.items() if value is not None}


def test_show_test_dfs(pl_df, connected, lengthMenu, monkeypatch):
    show(
        pl_df,
        connected=connected,
        **kwargs_remove_none(lengthMenu=lengthMenu),
    )


def test_to_html_datatable(pl_df, connected, lengthMenu, monkeypatch):
    to_html_datatable(
        pl_df,
        connected=connected,
        **kwargs_remove_none(lengthMenu=lengthMenu),
    )


def test_ordered_categories():
    df = get_dict_of_test_dfs()["ordered_categories"]
    df = df.sort("category", descending=True)
    assert (df["int"] == pl.Series("int", [3, 2, 1, 0])).all()


@pytest.mark.parametrize("series_name,series", get_dict_of_test_series().items())
def test_format_polars_series(
    series_name, series, escape_html, format_floats_in_python
):
    values = list(
        _format_polars_series(
            series,
            escape_html=escape_html,
            format_floats_in_python=format_floats_in_python,
            warn_on_polars_get_fmt_not_found=True,
        )
    )
    json.dumps(values, cls=generate_encoder())


@pytest.mark.parametrize("series_name,series", get_dict_of_test_series().items())
def test_show_test_series(series_name, series, connected, monkeypatch):
    show(series, connected=connected)


def test_polars_df_with_categorical_and_enums():
    cardinal_directions = pl.Enum(["north", "south", "east", "west"])
    df = pl.DataFrame(
        {
            "cat": pl.Series(["a", "b", "a", "c"], dtype=pl.Categorical),
            "enum": pl.Series(
                ["north", "south", "north", "west"], dtype=cardinal_directions
            ),
            "int": pl.Series([1, 2, 1, 3]),
        }
    )
    assert df.dtypes == [pl.Categorical, pl.Enum, pl.Int64]
    dt_args = get_itable_arguments(df)
    assert "data_json" in dt_args
    assert (
        dt_args["data_json"]
        == '[["a", "north", 1], ["b", "south", 2], ["a", "north", 1], ["c", "west", 3]]'
    )


def test_polars_df_with_nan_and_none():
    df = pl.DataFrame(
        {
            "A": [1, 2, None, 4],
            "B": [0.1, None, float("nan"), 0.4],
            "C": ["x", None, "z", "w"],
        }
    )
    assert df.dtypes == [pl.Int64, pl.Float64, pl.Utf8]
    dt_args = get_itable_arguments(df, format_floats_in_python=False)
    assert "data_json" in dt_args
    assert (
        dt_args["data_json"] == '[[1, 0.1, "x"], '
        '[2, null, "null"], '
        '[null, "___NaN___", "z"], '
        '[4, 0.4, "w"]]'
    )

    dt_args = get_itable_arguments(df)
    assert "data_json" in dt_args
    assert (
        dt_args["data_json"] == '[[1, {"display": "0.1", "sort": 0.1}, "x"], '
        '[2, {"display": "null", "sort": null}, "null"], '
        '[null, {"display": "NaN", "sort": "___NaN___"}, "z"], '
        '[4, {"display": "0.4", "sort": 0.4}, "w"]]'
    )
