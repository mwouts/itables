import itertools
import json
import math
import warnings
from datetime import date, datetime, timedelta

import pytest

from itables.datatables_format import datatables_rows, generate_encoder
from itables.javascript import (
    JavascriptCode,
    _column_count_in_header,
    _table_header,
    get_float_columns_to_be_formatted_in_python,
    get_itable_arguments,
)
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
        return (
            pd_or_pl.DataFrame({"x": [0.2, math.pi, math.nan, -math.inf]}),
            (
                (
                    '[[["0.200000", 2]], '
                    '[["3.141593", 3]], '
                    '[["NaN", 4]], '
                    '[["-inf", 1]]]'
                )
                if lib == "pd"
                else '[[["0.2", 2]], '
                '[["3.141593", 3]], '
                '[["NaN", 4]], '
                '[["-inf", 1]]]'
            ),
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
                [["2022-01-01"], ["null"]],
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
                [["2022-01-01 18:05:27"], ["null"]],
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
                [["2022-01-01 18:05:27 EST"], ["null"]],
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
                [["1h"], ["null"]],
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
                [["{1,null}"], ["{null,[1, 2]}"]],
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
    df_module_name = get_dataframe_module_name(df)
    table_header = _table_header(
        df,
        df_module_name=df_module_name,
        show_index=False,
        footer=False,
        column_filters=False,
        escape_html=True,
        show_dtypes=False,
    )
    column_count = _column_count_in_header(table_header)
    float_columns_to_be_formatted_in_python = (
        get_float_columns_to_be_formatted_in_python(df_module_name, df, True, [])
    )
    actual = datatables_rows(
        df,
        column_count=column_count,
        float_columns_to_be_formatted_in_python=float_columns_to_be_formatted_in_python,
    )
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
    assert datatables_rows(df, float_columns_to_be_formatted_in_python={2, 3}) == (
        "[[1666767918216000000, 1699300000000, "
        '["0.951057", 1], '
        '["-0.309017", 1]]]'
    )
    assert datatables_rows(df, float_columns_to_be_formatted_in_python=set()) == (
        "[[1666767918216000000, 1699300000000, 0.9510565400123596, -0.30901700258255005]]"
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
    assert datatables_rows(df, float_columns_to_be_formatted_in_python={2, 3}) == (
        "[[1666767918216000000, 1699300000000, "
        '["0.951057", 1], '
        '["-0.309017", 1]]]'
    )

    assert datatables_rows(df, float_columns_to_be_formatted_in_python=set()) == (
        "[[1666767918216000000, 1699300000000, 0.9510565400123596, -0.30901700258255005]]"
    )


def test_polars_float_formatting():
    """Make sure that polars float formatting is compatible with datatables_rows"""
    try:
        import polars as pl
    except ImportError:
        pytest.skip("polars is not installed")

    df = pl.DataFrame({"float": [math.pi, math.pi * 1e12]})
    assert datatables_rows(df, float_columns_to_be_formatted_in_python={0}) == (
        '[[["3.141593", 1]], ' '[["3.1416e12", 2]]]'
    )

    with pl.Config(float_precision=12):
        assert datatables_rows(df, float_columns_to_be_formatted_in_python={0}) == (
            '[[["3.141592653590", 1]], ' '[["3.141592653590e12", 2]]]'
        )


def test_polars_array_float_formatting():
    """Test that Polars float_precision config applies to Array[Float64] columns, cf. #471"""
    try:
        import polars as pl
    except ImportError:
        pytest.skip("polars is not installed")

    # Test with Array[Float64]
    df = pl.DataFrame(
        {"array_col": [[1.234567890123456, 2.345678901234567, math.pi]]},
        schema={"array_col": pl.Array(pl.Float64, 3)},
    )

    # Default formatting - Polars default precision (6 decimal places)
    result = datatables_rows(df)
    assert "[1.234568, 2.345679, 3.141593]" in result

    # With precision=2
    with pl.Config(float_precision=2):
        result = datatables_rows(df)
        assert "[1.23, 2.35, 3.14]" in result

    # With precision=10
    with pl.Config(float_precision=10):
        result = datatables_rows(df)
        assert "[1.2345678901, 2.3456789012, 3.1415926536]" in result


def test_polars_list_float_formatting():
    """Test that Polars float_precision config applies to List[Float64] columns, cf. #471"""
    try:
        import polars as pl
    except ImportError:
        pytest.skip("polars is not installed")

    # Test with List[Float64]
    df = pl.DataFrame(
        {
            "list_col": [
                [1.234567890123456, 2.345678901234567, math.pi],
                [4.5, 6.7],
            ]
        }
    )

    # Default formatting - Polars default precision (6 decimal places)
    result = datatables_rows(df)
    assert "[1.234568, 2.345679, 3.141593]" in result
    assert "[4.5, 6.7]" in result

    # With precision=2
    with pl.Config(float_precision=2):
        result = datatables_rows(df)
        assert "[1.23, 2.35, 3.14]" in result
        # Note: 4.5 and 6.7 become 4.50 and 6.70 with precision=2
        assert "[4.50, 6.70]" in result

    # With precision=10
    with pl.Config(float_precision=10):
        result = datatables_rows(df)
        assert "[1.2345678901, 2.3456789012, 3.1415926536]" in result
        assert "[4.5000000000, 6.7000000000]" in result


def test_polars_array_list_with_non_finite_floats():
    """Test that non-finite floats in arrays/lists are properly escaped"""
    try:
        import polars as pl
    except ImportError:
        pytest.skip("polars is not installed")

    # Test with Array containing NaN, Inf, -Inf
    df_array = pl.DataFrame(
        {"array_col": [[1.5, math.nan, math.inf, -math.inf, 2.5]]},
        schema={"array_col": pl.Array(pl.Float64, 5)},
    )
    result = datatables_rows(df_array)
    assert result == '[["[1.5, NaN, \\u2026 2.5]"]]'

    # Test with List containing NaN, Inf
    df_list = pl.DataFrame({"list_col": [[1.5, math.nan, math.inf], [-math.inf, 2.5]]})
    result = datatables_rows(df_list)
    assert result == '[["[1.5, NaN, inf]"], ["[-inf, 2.5]"]]'


def test_polars_list_with_none_values():
    """Test that None values in list columns are handled correctly"""
    try:
        import polars as pl
    except ImportError:
        pytest.skip("polars is not installed")

    df = pl.DataFrame({"list_col": [[1.5, 2.5], None, [3.5]]})

    # Default formatting
    result = datatables_rows(df)
    assert result == '[["[1.5, 2.5]"], ["null"], ["[3.5]"]]'

    # With precision - Polars adds trailing zeros to match precision
    with pl.Config(float_precision=2):
        result = datatables_rows(df)
        assert result == '[["[1.50, 2.50]"], ["null"], ["[3.50]"]]'


def test_show_dtypes_pandas():
    pd = pytest.importorskip("pandas")
    df = pd.DataFrame({"a": [1], "b": [2]})
    dt_args = get_itable_arguments(df, show_dtypes=True)
    assert "table_html" in dt_args
    assert (
        "<tr><th><small class='itables-dtype'>i64</small></th><th><small class='itables-dtype'>i64</small></th>"
        in dt_args["table_html"]
    )

    df = pd.DataFrame({"a": [1], "b": [2]}, index=pd.Index(["O"], name="index"))
    dt_args = get_itable_arguments(df, show_dtypes=True)
    assert "table_html" in dt_args
    assert (
        "<tr><th><small class='itables-dtype'>object</small></th><th><small class='itables-dtype'>i64</small></th><th><small class='itables-dtype'>i64</small></th>"
        in dt_args["table_html"]
    )


def test_show_dtypes_polars():
    pl = pytest.importorskip("polars")
    df = pl.DataFrame({"a": [1]})
    dt_args = get_itable_arguments(df)
    assert "table_html" in dt_args
    assert "i64" in dt_args["table_html"]

    df = pl.DataFrame({"a": [1]}, schema={"a": pl.UInt32})
    dt_args = get_itable_arguments(df)
    assert "table_html" in dt_args
    assert "u32" in dt_args["table_html"]

    df = pl.DataFrame({"a": [1], "b": [2]})
    with pl.Config(tbl_hide_column_data_types=True):
        dt_args = get_itable_arguments(df)
    assert "table_html" in dt_args
    assert "64" not in dt_args["table_html"]


def test_render_in_columndefs_deactivates_python_float_formatting_polars():
    pl = pytest.importorskip("polars")
    df = pl.DataFrame(
        {
            "bigint": [1666767918216000000],
            "int": [1699300000000],
            "float": [0.9510565400123596],
            "neg": [-0.30901700258255005],
        }
    )
    float_columns = get_float_columns_to_be_formatted_in_python(
        df_module_name="polars",
        df=df,
        format_floats_in_python="auto",
        columnDefs=[],
    )
    assert float_columns == {2, 3}
    columnDefs = [
        {
            "targets": 2,
            "render": "function(data, type, row, meta) { return data.toFixed(3); }",
        },
        {
            "targets": 3,
            "render": "function(data, type, row, meta) { return data.toFixed(3); }",
        },
    ]
    float_columns = get_float_columns_to_be_formatted_in_python(
        df_module_name="polars",
        df=df,
        format_floats_in_python="auto",
        columnDefs=columnDefs,
    )
    assert float_columns == set()


def test_render_in_columndefs_deactivates_python_float_formatting_pandas():
    pd = pytest.importorskip("pandas")
    df = pd.DataFrame(
        {"int": range(1, 6), "float": [i * math.pi * 1e4 for i in range(1, 6)]}
    )

    float_columns = get_float_columns_to_be_formatted_in_python(
        df_module_name="pandas",
        df=df,
        format_floats_in_python="auto",
        columnDefs=[],
    )
    assert float_columns == {1}
    columnDefs = [
        {
            "targets": 1,
            "render": JavascriptCode("$.fn.dataTable.render.number(',', '.', 3, '$')"),
        }
    ]
    float_columns = get_float_columns_to_be_formatted_in_python(
        df_module_name="pandas",
        df=df,
        format_floats_in_python="auto",
        columnDefs=columnDefs,
    )
    assert float_columns == set()


@pytest.mark.parametrize("dataframe_library", ["pandas", "polars"])
def test_long_strings_are_not_truncated(dataframe_library: str):
    """Test that long strings are passed verbatim to itables for Pandas"""
    pd_or_pl = pytest.importorskip(dataframe_library)

    # Create a dataframe with a long string that exceeds the typical truncation length
    long_string = (
        "This is a very long string that should not be truncated by itables formatting. "
        * 50
    )
    df = pd_or_pl.DataFrame({"text": [long_string]})

    # Get the formatted rows
    result = datatables_rows(df)

    # The result should contain the full string
    assert (
        long_string in result
    ), f"Long string was truncated in {dataframe_library} dataframe"
