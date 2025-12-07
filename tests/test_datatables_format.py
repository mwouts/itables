import itertools
import json
import math
import warnings
from datetime import date, datetime, timedelta

import pytest

from itables.datatables_format import datatables_rows, generate_encoder
from itables.javascript import _column_count_in_header, _table_header
from itables.typing import get_dataframe_module_name


@pytest.fixture(
    params=itertools.product(
        [
            "bool",
            "nullable_bool",
            "int",
            "nullable_int",
            "float",
            "str",
            "date",
            "datetime",
            "datetime_with_tz",
            "timedelta",
            "object_list",
            "object_dict",
            "df_with_named_column_axis",
            "transposed_df",
            "big_integers",
        ],
        ["pd", "pl"],
    ),
    ids=lambda param: "_".join(param),
)
def df_and_expected(request):
    id, lib = request.param

    if lib == "pd":
        try:
            import pandas as pd

            pd_or_pl = pd
            pl = None
        except ImportError:
            pytest.skip("pandas is not installed")
            pd_or_pl = pd = pl = None
    else:
        try:
            import polars as pl

            pd_or_pl = pl
            pd = None
        except ImportError:
            pytest.skip("polars is not installed")
            pd_or_pl = pd = pl = None

    assert pd_or_pl is not None
    if id == "bool":
        return pd_or_pl.DataFrame({"x": [True, False]}), [[True], [False]]
    elif id == "nullable_bool":
        if lib == "pd":
            assert pd is not None
            return (
                pd.DataFrame(
                    {"x": [True, False, None]},
                    dtype="boolean",
                ),
                [[True], [False], ["<NA>"]],
            )
        else:
            assert pl is not None
            return (pl.DataFrame({"x": [True, False, None]}), [[True], [False], [None]])
    elif id == "int":
        return pd_or_pl.DataFrame({"x": [0, 1]}), [[0], [1]]
    elif id == "nullable_int":
        if lib == "pd":
            assert pd is not None
            return (
                pd.DataFrame({"x": [0, 1, None]}, dtype="Int64"),
                [[0], [1], ["<NA>"]],
            )
        else:
            assert pl is not None
            return (pl.DataFrame({"x": [0, 1, None]}), [[0], [1], [None]])
    elif id == "float":
        if lib == "pd":
            assert pd is not None
            return (
                pd.DataFrame({"x": [0.2, math.pi, math.nan, -math.inf]}),
                '[[0.2], [3.141593], ["___NaN___"], ["___-Infinity___"]]',
            )
        else:
            assert pl is not None
            return (
                pl.DataFrame({"x": [0.2, math.pi, math.nan, -math.inf]}),
                '[[0.2], [3.141592653589793], ["___NaN___"], ["___-Infinity___"]]',
            )
    elif id == "str":
        return (pd_or_pl.DataFrame({"s": ["hi", '"hi"']}), [["hi"], ['"hi"']])
    elif id == "date":
        if lib == "pd":
            assert pd is not None
            return (
                pd.DataFrame({"d": [date(2022, 1, 1), pd.NaT]}),
                [["2022-01-01"], ["NaT"]],
            )
        else:
            assert pl is not None
            return (
                pl.DataFrame({"d": [date(2022, 1, 1), None]}),
                [["2022-01-01"], [None]],
            )
    elif id == "datetime":
        if lib == "pd":
            assert pd is not None
            return (
                pd.DataFrame({"t": [datetime(2022, 1, 1, 18, 5, 27), pd.NaT]}),
                [["2022-01-01 18:05:27"], ["NaT"]],
            )
        else:
            assert pl is not None
            return (
                pl.DataFrame({"t": [datetime(2022, 1, 1, 18, 5, 27), None]}),
                [["2022-01-01 18:05:27.000000"], [None]],
            )
    elif id == "datetime_with_tz":
        if lib == "pd":
            assert pd is not None
            return (
                pd.DataFrame(
                    {
                        "t": pd.to_datetime(
                            [datetime(2022, 1, 1, 18, 5, 27), pd.NaT]  # type: ignore
                        ).tz_localize("US/Eastern")
                    }
                ),
                [["2022-01-01 18:05:27-05:00"], ["NaT"]],
            )
        else:
            try:
                from pytz import timezone
            except ImportError:
                pytest.skip("pytz is not installed")
            assert pl is not None
            return (
                pl.DataFrame(
                    {
                        "t": [
                            datetime(2022, 1, 1, 18, 5, 27),
                            None,
                        ]
                    }
                ).with_columns(
                    pl.col("t").dt.replace_time_zone(timezone("US/Eastern").zone)
                ),
                [["2022-01-01 18:05:27.000000-05:00"], [None]],
            )
    elif id == "timedelta":
        if lib == "pd":
            assert pd is not None
            return (
                pd.DataFrame({"dt": [pd.Timedelta(1, unit="h"), pd.NaT - pd.NaT]}),  # type: ignore
                [["0 days 01:00:00"], ["NaT"]],
            )
        else:
            assert pl is not None
            return (
                pl.DataFrame({"dt": [timedelta(hours=1), None]}),
                [["1:00:00"], [None]],
            )
    elif id == "object_list":
        return (pd_or_pl.DataFrame({"list": [[1], [2, 3]]}), [["[1]"], ["[2, 3]"]])
    elif id == "object_dict":
        if lib == "pd":
            assert pd is not None
            return (
                pd.DataFrame({"dict": [{"a": 1}, {"b": [1, 2]}]}),
                [["{'a': 1}"], ["{'b': [1, 2]}"]],
            )
        else:
            assert pl is not None
            return (
                pl.DataFrame({"dict": [{"a": 1, "b": None}, {"b": [1, 2]}]}),
                [["{'a': 1, 'b': None}"], ["{'a': None, 'b': [1, 2]}"]],
            )
    elif id == "df_with_named_column_axis":
        if lib == "pl":
            pytest.skip("Polars does not support named axes")
        assert pd is not None
        return (pd.DataFrame({"a": [1]}).rename_axis("columns", axis=1), [[None, 1]])
    elif id == "transposed_df":
        if lib == "pl":
            pytest.skip("Polars does not support named axes")
        assert pd is not None
        return (
            pd.DataFrame({"a": [1, 2]}, index=pd.Index([1, 2], name="index"))
            .rename_axis("columns", axis=1)
            .T.reset_index(),
            [[None, "a", 1, 2]],
        )
    elif id == "big_integers":
        return (
            pd_or_pl.DataFrame(
                {
                    "big_integers": [
                        1234567890123456789,
                        2345678901234567890,
                        3456789012345678901,
                    ]
                }
            ),
            "[[1234567890123456789], [2345678901234567890], [3456789012345678901]]",
        )


@pytest.fixture()
def df(df_and_expected):
    return df_and_expected[0]


@pytest.fixture()
def expected(df_and_expected):
    return df_and_expected[1]


def test_datatables_rows(df, expected):
    table_header = _table_header(
        df,
        df_module_name=get_dataframe_module_name(df),
        show_index=False,
        footer=False,
        column_filters=False,
        escape_html=True,
    )
    column_count = _column_count_in_header(table_header)
    actual = datatables_rows(df, column_count=column_count)
    if isinstance(expected, str):
        assert actual == expected
    else:
        assert actual == json.dumps(expected)


def test_TableValuesEncoder():
    assert json.dumps(['"str"'], cls=generate_encoder()) == r'["\"str\""]'
    with pytest.warns(RuntimeWarning, match="Unexpected type"):
        json.dumps(Exception, cls=generate_encoder())

    with warnings.catch_warnings():
        warnings.simplefilter("error")
        assert (
            json.dumps(Exception, cls=generate_encoder(False))
            == "\"<class 'Exception'>\""
        )


def test_encode_large_int(large=3456789012345678901):
    """Encoding large integers from Python using json.dumps works"""
    assert json.dumps([large]) == "[3456789012345678901]"
    assert (
        json.dumps([large * 100, large])
        == "[345678901234567890100, 3456789012345678901]"
    )


def test_encode_mixed_contents_pandas():
    # Make sure that the bigint escape works for mixed content # 291
    try:
        import pandas as pd
    except ImportError:
        pytest.skip("pandas is not installed")
    df = pd.DataFrame(
        {
            "bigint": [1666767918216000000],
            "int": [1699300000000],
            "float": [0.9510565400123596],
            "neg": [-0.30901700258255005],
        }
    )
    assert (
        datatables_rows(df)
        == "[[1666767918216000000, 1699300000000, 0.951057, -0.309017]]"
    )


def test_encode_mixed_contents_polars():
    # Make sure that the bigint escape works for mixed content # 291
    try:
        import polars as pl
    except ImportError:
        pytest.skip("polars is not installed")
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


def test_polars_float_formatting():
    """Make sure that polars float formatting is compatible with datatables_rows"""
    try:
        import polars as pl
    except ImportError:
        pytest.skip("polars is not installed")

    df = pl.DataFrame({"float": [math.pi, math.pi * 1e12]})
    assert datatables_rows(df) == "[[3.141592653589793], [3141592653589.793]]"

    with pl.Config(float_precision=6):
        assert datatables_rows(df) == "[[3.141593], [3141592653589.793]]"
