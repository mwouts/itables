import json
import math
import sys
import warnings
from datetime import date, datetime

import numpy as np
import pandas as pd
import pytest

import itables.options as opt
from itables.datatables_format import TableValuesEncoder, datatables_rows


@pytest.mark.skipif(
    sys.version_info < (3,), reason="pandas formatting has changed since Py2"
)
@pytest.mark.parametrize(
    "df,expected",
    [
        (pd.DataFrame({"x": [True, False]}), [[True], [False]]),
        (
            pd.DataFrame(
                {"x": [True, False, None]},
                dtype="boolean" if sys.version_info > (3,) else "bool",
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
    ],
)
def test_datatables_rows(df, expected):
    actual = datatables_rows(df)
    assert actual == json.dumps(expected)


@pytest.mark.skipif(
    sys.version_info < (3,), reason="str(Exception) has changed since Py2"
)
def test_TableValuesEncoder():
    assert json.dumps(['"str"'], cls=TableValuesEncoder) == r'["\"str\""]'
    with pytest.warns(RuntimeWarning, match="Unexpected type"):
        json.dumps(Exception, cls=TableValuesEncoder)

    opt.warn_on_unexpected_types = False
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        assert (
            json.dumps(Exception, cls=TableValuesEncoder) == "\"<class 'Exception'>\""
        )
