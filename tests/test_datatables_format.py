import json
import math
import warnings
from datetime import date, datetime

import numpy as np
import pandas as pd
import pytest

from itables.datatables_format import datatables_rows, generate_encoder
from itables.javascript import _column_count_in_header, _table_header
from itables.sample_dfs import PANDAS_VERSION_MAJOR


@pytest.mark.skipif(
    PANDAS_VERSION_MAJOR == 0, reason="pandas formats have changed in pandas==1.0"
)
@pytest.mark.parametrize(
    "df,expected",
    [
        (pd.DataFrame({"x": [True, False]}), [[True], [False]]),
        (
            pd.DataFrame(
                {"x": [True, False, None]},
                dtype="bool" if PANDAS_VERSION_MAJOR == 0 else "boolean",
            ),
            [[True], [False], ["<NA>"]],
        ),
        (pd.DataFrame({"x": [0, 1]}), [[0], [1]]),
        (pd.DataFrame({"x": [0, 1, None]}, dtype="Int64"), [[0], [1], ["<NA>"]]),
        (
            pd.DataFrame({"x": [0.2, math.pi, np.nan, -np.inf]}),
            '[[0.2], [3.141593], ["___NaN___"], ["___-Infinity___"]]',
        ),
        (pd.DataFrame({"s": ["hi", '"hi"']}), [["hi"], ['"hi"']]),
        (pd.DataFrame({"t": [date(2022, 1, 1), pd.NaT]}), [["2022-01-01"], ["NaT"]]),
        (
            pd.DataFrame({"t": [datetime(2022, 1, 1, 18, 5, 27), pd.NaT]}),
            [["2022-01-01 18:05:27"], ["NaT"]],
        ),
        (
            pd.DataFrame(
                {
                    "t": pd.to_datetime(
                        [datetime(2022, 1, 1, 18, 5, 27), pd.NaT]  # type: ignore
                    ).tz_localize("US/Eastern")
                }
            ),
            [["2022-01-01 18:05:27-05:00"], ["NaT"]],
        ),
        (
            pd.DataFrame({"dt": [pd.Timedelta(1, unit="h"), pd.NaT - pd.NaT]}),  # type: ignore
            [["0 days 01:00:00"], ["NaT"]],
        ),
        (pd.DataFrame({"list": [[1], [2, 3]]}), [["[1]"], ["[2, 3]"]]),
        (
            pd.DataFrame({"dict": [{"a": 1}, {"b": [1, 2]}]}),
            [["{'a': 1}"], ["{'b': [1, 2]}"]],
        ),
        (pd.DataFrame({"a": [1]}).rename_axis("columns", axis=1), [[None, 1]]),
        (
            pd.DataFrame({"a": [1, 2]}, index=pd.Index([1, 2], name="index"))
            .rename_axis("columns", axis=1)
            .T.reset_index(),
            [[None, "a", 1, 2]],
        ),
        (
            pd.DataFrame(
                {
                    "big_integers": [
                        1234567890123456789,
                        2345678901234567890,
                        3456789012345678901,
                    ]
                }
            ),
            "[[1234567890123456789], [2345678901234567890], [3456789012345678901]]",
        ),
    ],
    ids=[
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
)
def test_datatables_rows(df, expected):
    table_header = _table_header(
        df,
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


def test_encode_mixed_contents():
    # Make sure that the bigint escape works for mixed content # 291
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
