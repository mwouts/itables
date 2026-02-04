"""Tests for Narwhals integration"""

from typing import cast

import pytest

from itables.datatables_format import datatables_rows
from itables.javascript import get_itable_arguments, to_html_datatable


def test_narwhals_dataframe_via_pandas():
    """Test that we can display a DataFrame via narwhals using pandas backend"""
    pd = pytest.importorskip("pandas")
    nw = pytest.importorskip("narwhals")

    # Create a simple pandas DataFrame
    df_pandas = pd.DataFrame({"A": [1, 2, 3], "B": [4.0, 5.0, 6.0]})
    df_nw = nw.from_native(df_pandas)

    # The rows should be the same
    dr_nw = datatables_rows(df_nw)
    dr_pd = datatables_rows(df_pandas)

    assert dr_nw == dr_pd


def test_cudf_dataframe():
    """Test that we can display a cudf DataFrame"""
    cudf = pytest.importorskip("cudf")
    pytest.importorskip("narwhals")

    # Create a simple cudf DataFrame
    df_cudf = cudf.DataFrame({"A": [1, 2, 3], "B": [4.0, 5.0, 6.0]})
    assert datatables_rows(df_cudf) == "[[1, 4.0], [2, 5.0], [3, 6.0]]"
    to_html_datatable(df_cudf)


def test_pyarrow_table():
    """Test that we can display a pyarrow Table"""
    pa = pytest.importorskip("pyarrow")
    pytest.importorskip("narwhals")

    # Create a simple pyarrow Table
    table = pa.table({"A": [1, 2, 3], "B": [4.0, 5.0, 6.0]})
    assert datatables_rows(table) == "[[1, 4.0], [2, 5.0], [3, 6.0]]"
    to_html_datatable(table)


def test_modin_dataframe():
    """Test that we can display a modin DataFrame"""
    modin = pytest.importorskip("modin.pandas")
    pytest.importorskip("narwhals")

    # Create a simple modin DataFrame
    df_modin = modin.DataFrame({"A": [1, 2, 3], "B": [4.0, 5.0, 6.0]})
    assert datatables_rows(df_modin) == "[[1, 4.0], [2, 5.0], [3, 6.0]]"
    to_html_datatable(df_modin)

    assert (
        datatables_rows(df_modin, float_columns_to_be_formatted_in_python={1})
        == '[[1, {"display": "4.0", "sort": 1}], [2, {"display": "5.0", "sort": 2}], [3, {"display": "6.0", "sort": 3}]]'
    )


def test_pandas_dataframe_same_through_narwhals_df():
    pd = pytest.importorskip("pandas")
    nw = pytest.importorskip("narwhals")

    df = pd.DataFrame({"A": [1, 2, 3], "B": [4.0, 5.0, 6.0]}, index=["a", "b", "c"])
    it_args = get_itable_arguments(df, show_df_type=True)

    df_nw = nw.from_native(df)
    it_args_nw = get_itable_arguments(df_nw, show_df_type=True)
    assert "downsampling_warning" in it_args
    it_args["downsampling_warning"] = (
        cast(str, it_args["downsampling_warning"]) + " (narwhalified)"
    )
    assert it_args == it_args_nw


def test_pandas_series_same_through_narwhals():
    pd = pytest.importorskip("pandas")
    nw = pytest.importorskip("narwhals")

    s = pd.Series([1, 2, 3], name="A", index=["a", "b", "c"])
    it_args = get_itable_arguments(s, show_df_type=True)

    s_nw = nw.from_native(s, allow_series=True)
    it_args_nw = get_itable_arguments(s_nw, show_df_type=True)
    assert "downsampling_warning" in it_args
    it_args["downsampling_warning"] = (
        cast(str, it_args["downsampling_warning"]) + " (narwhalified)"
    )
    assert it_args == it_args_nw


def test_dataframe_type_pandas_df():
    pd = pytest.importorskip("pandas")

    df = pd.DataFrame({"A": [1, 2, 3], "B": [4.0, 5.0, 6.0]})
    it_args = get_itable_arguments(df, show_df_type=True)
    assert "downsampling_warning" in it_args
    assert it_args["downsampling_warning"] == "pandas.DataFrame"

    nw = pytest.importorskip("narwhals")
    df_nw = nw.from_native(df)
    it_args_nw = get_itable_arguments(df_nw, show_df_type=True)
    assert "downsampling_warning" in it_args_nw
    assert it_args_nw["downsampling_warning"] == "pandas.DataFrame (narwhalified)"


def test_dataframe_type_pandas_series():
    pd = pytest.importorskip("pandas")

    x = pd.Series([1, 2, 3], name="A")
    it_args = get_itable_arguments(x, show_df_type=True)
    assert "downsampling_warning" in it_args
    assert it_args["downsampling_warning"] == "pandas.Series"

    nw = pytest.importorskip("narwhals")
    x_nw = nw.from_native(x, allow_series=True)
    it_args_nw = get_itable_arguments(x_nw, show_df_type=True)
    assert "downsampling_warning" in it_args_nw
    assert it_args_nw["downsampling_warning"] == "pandas.Series (narwhalified)"


def test_dataframe_type_numpy_array():
    np = pytest.importorskip("numpy")

    arr = np.array([[1, 4.0], [2, 5.0], [3, 6.0]])
    it_args = get_itable_arguments(arr, show_df_type=True)
    assert "downsampling_warning" in it_args
    assert it_args["downsampling_warning"] == "numpy.ndarray"


def test_dataframe_type_polars_df():
    pl = pytest.importorskip("polars")

    df = pl.DataFrame({"A": [1, 2, 3], "B": [4.0, 5.0, 6.0]})
    it_args = get_itable_arguments(df, show_df_type=True)
    assert "downsampling_warning" in it_args
    assert it_args["downsampling_warning"] == "polars.DataFrame"

    nw = pytest.importorskip("narwhals")
    df_nw = nw.from_native(df)
    it_args_nw = get_itable_arguments(df_nw, show_df_type=True)
    assert "downsampling_warning" in it_args_nw
    assert it_args_nw["downsampling_warning"] == "polars.DataFrame (narwhalified)"


def test_dataframe_type_polars_series():
    pl = pytest.importorskip("polars")

    x = pl.Series([1, 2, 3])
    it_args = get_itable_arguments(x, show_df_type=True)
    assert "downsampling_warning" in it_args
    assert it_args["downsampling_warning"] == "polars.Series"

    nw = pytest.importorskip("narwhals")
    x_nw = nw.from_native(x, allow_series=True)
    it_args_nw = get_itable_arguments(x_nw, show_df_type=True)
    assert "downsampling_warning" in it_args_nw
    assert it_args_nw["downsampling_warning"] == "polars.Series (narwhalified)"


def test_dataframe_type_cudf_df():
    cudf = pytest.importorskip("cudf")

    df = cudf.DataFrame({"A": [1, 2, 3], "B": [4.0, 5.0, 6.0]})
    it_args = get_itable_arguments(df, show_df_type=True)
    assert "downsampling_warning" in it_args
    assert it_args["downsampling_warning"] == "cudf.DataFrame"

    nw = pytest.importorskip("narwhals")
    df_nw = nw.from_native(df, show_df_type=True)
    it_args_nw = get_itable_arguments(df_nw)
    assert "downsampling_warning" in it_args_nw
    assert it_args_nw["downsampling_warning"] == "cudf.DataFrame (narwhalified)"


def test_dataframe_type_pyarrow_table():
    pa = pytest.importorskip("pyarrow")

    table = pa.table({"A": [1, 2, 3], "B": [4.0, 5.0, 6.0]})
    it_args = get_itable_arguments(table, show_df_type=True)
    assert "downsampling_warning" in it_args
    assert it_args["downsampling_warning"] == "pyarrow.Table"

    nw = pytest.importorskip("narwhals")
    table_nw = nw.from_native(table)
    it_args_nw = get_itable_arguments(table_nw, show_df_type=True)
    assert "downsampling_warning" in it_args_nw
    assert it_args_nw["downsampling_warning"] == "pyarrow.Table (narwhalified)"


def test_dataframe_type_modin_df():
    modin = pytest.importorskip("modin.pandas")

    df = modin.DataFrame({"A": [1, 2, 3], "B": [4.0, 5.0, 6.0]})
    it_args = get_itable_arguments(df, show_df_type=True)
    assert "downsampling_warning" in it_args
    assert it_args["downsampling_warning"] == "modin.pandas.DataFrame"

    nw = pytest.importorskip("narwhals")
    df_nw = nw.from_native(df)
    it_args_nw = get_itable_arguments(df_nw, show_df_type=True)
    assert "downsampling_warning" in it_args_nw
    assert it_args_nw["downsampling_warning"] == "modin.pandas.DataFrame (narwhalified)"
