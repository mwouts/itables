"""Tests for Narwhals integration"""

import pytest

from itables.datatables_format import datatables_rows
from itables.javascript import to_html_datatable

nw = pytest.importorskip("narwhals")


def test_narwhals_dataframe_via_pandas():
    """Test that we can display a DataFrame via narwhals using pandas backend"""
    pd = pytest.importorskip("pandas")

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

    # Create a simple cudf DataFrame
    df_cudf = cudf.DataFrame({"A": [1, 2, 3], "B": [4.0, 5.0, 6.0]})
    assert datatables_rows(df_cudf) == "[[1, 4.0], [2, 5.0], [3, 6.0]]"
    to_html_datatable(df_cudf)


def test_pyarrow_table():
    """Test that we can display a pyarrow Table"""
    pa = pytest.importorskip("pyarrow")

    # Create a simple pyarrow Table
    table = pa.table({"A": [1, 2, 3], "B": [4.0, 5.0, 6.0]})
    assert datatables_rows(table) == "[[1, 4.0], [2, 5.0], [3, 6.0]]"
    to_html_datatable(table)


def test_modin_dataframe():
    """Test that we can display a modin DataFrame"""
    modin = pytest.importorskip("modin.pandas")

    # Create a simple modin DataFrame
    df_modin = modin.DataFrame({"A": [1, 2, 3], "B": [4.0, 5.0, 6.0]})
    assert datatables_rows(df_modin) == "[[1, 4.0], [2, 5.0], [3, 6.0]]"
    to_html_datatable(df_modin)
