import json
import math
import warnings
from datetime import date, datetime

import numpy as np
import pandas as pd
import pytest

from itables.datatables_format import (
    JS_MAX_SAFE_INTEGER,
    JS_MIN_SAFE_INTEGER,
    datatables_rows,
    generate_encoder,
    n_suffix_for_bigints,
)
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
            pd.DataFrame({"x": [0.2, math.pi, np.NaN, -np.Infinity]}),
            [[0.2], [round(math.pi, 6)], [float("NaN")], [-float("inf")]],
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
                        [datetime(2022, 1, 1, 18, 5, 27), pd.NaT]
                    ).tz_localize("US/Eastern")
                }
            ),
            [["2022-01-01 18:05:27-05:00"], ["NaT"]],
        ),
        (
            pd.DataFrame({"dt": [pd.Timedelta(1, unit="h"), pd.NaT - pd.NaT]}),
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
            '[[BigInt("1234567890123456789")], [BigInt("2345678901234567890")], [BigInt("3456789012345678901")]]',
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
        table_id="",
        show_index=False,
        classes="",
        style="",
        tags="",
        footer=False,
        column_filters=False,
        connected=False,
        display_logo_when_loading=False,
    )
    column_count = _column_count_in_header(table_header)
    actual = datatables_rows(df, count=column_count)
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


def test_encode_large_int_to_bigint(large=3456789012345678901):
    assert (
        n_suffix_for_bigints(json.dumps([large])) == '[BigInt("3456789012345678901")]'
    )
    assert (
        n_suffix_for_bigints(json.dumps([large * 100, large]))
        == '[BigInt("345678901234567890100"), BigInt("3456789012345678901")]'
    )


@pytest.mark.parametrize("large", [JS_MIN_SAFE_INTEGER, JS_MAX_SAFE_INTEGER])
def test_encode_max_int(large):
    assert n_suffix_for_bigints(json.dumps([large])) == '[BigInt("{}")]'.format(large)


@pytest.mark.parametrize("large", [JS_MIN_SAFE_INTEGER, JS_MAX_SAFE_INTEGER])
def test_encode_not_max_int(large):
    large //= 10
    assert n_suffix_for_bigints(json.dumps([large])) == "[{}]".format(large)
