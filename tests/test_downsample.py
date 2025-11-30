"""Test that the code in all the test notebooks work, including README.md"""

import pytest

try:
    import pandas as pd

    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False
    pd = None

try:
    import polars as pl

    POLARS_AVAILABLE = True
except ImportError:
    POLARS_AVAILABLE = False
    pl = None

if not PANDAS_AVAILABLE and not POLARS_AVAILABLE:
    pytest.skip("Neither Pandas nor Polars is available", allow_module_level=True)

from itables.downsample import (
    as_nbytes,
    downsample,
    nbytes,
    shrink_towards_target_aspect_ratio,
)


def test_as_nbytes():
    assert as_nbytes(0) == 0
    assert as_nbytes(2**16) == 2**16
    assert as_nbytes("256B") == 256
    assert as_nbytes("64KB") == 2**16
    assert as_nbytes("1MB") == 2**20


def large_tables(N=1000, M=1000):
    dfs = []
    if PANDAS_AVAILABLE:
        dfs.extend(
            [
                pd.DataFrame(5, columns=range(M), index=range(N)),
                pd.DataFrame(3.14159, columns=range(M), index=range(N)),
                pd.DataFrame("abcdefg", columns=range(M), index=range(N)),
            ]
        )
    if POLARS_AVAILABLE:
        if PANDAS_AVAILABLE:
            dfs.extend([pl.from_pandas(df) for df in dfs[:3]])  # type: ignore
        else:

            dfs.extend(
                [
                    pl.DataFrame({str(i): [5] * N for i in range(M)}),
                    pl.DataFrame({str(i): [3.14159] * N for i in range(M)}),
                    pl.DataFrame({str(i): ["abcdefg"] * N for i in range(M)}),
                ]
            )
    return dfs


@pytest.mark.parametrize("df", large_tables())
@pytest.mark.parametrize("max_rows", [99, 100])
def test_max_rows(df, max_rows):
    dn, message = downsample(df, max_rows=max_rows)
    assert len(dn) == max_rows
    try:
        pd.testing.assert_index_equal(dn.columns, df.columns)  # type: ignore
    except AssertionError:
        assert dn.columns == df.columns


@pytest.mark.parametrize("df", large_tables())
@pytest.mark.parametrize("max_columns", [99, 100])
def test_max_columns(df, max_columns):
    dn, message = downsample(df, max_columns=max_columns)
    assert len(dn.columns) == max_columns
    try:
        pd.testing.assert_index_equal(dn.index, df.index)  # type: ignore
    except AttributeError:
        assert len(dn) == len(df)


@pytest.mark.parametrize("df", large_tables())
@pytest.mark.parametrize("max_bytes", [10, 1e2, 1e3, 1e4, 1e5])
def test_max_bytes(df, max_bytes):
    dn, message = downsample(df, max_bytes=max_bytes)
    assert nbytes(dn) <= max_bytes + 9
    assert nbytes(dn) > max_bytes / 2


@pytest.mark.parametrize("df", large_tables())
def test_max_one_byte(df, max_bytes=1):
    dn, message = downsample(df, max_bytes=max_bytes)
    assert len(dn.columns) == len(dn) == 1
    try:
        assert dn.iloc[0, 0] == "..."  # type: ignore
    except AttributeError:
        assert dn[0, df.columns[0]] == "..."  # type: ignore


def test_shrink_towards_target_aspect_ratio():
    # Shrink on rows only
    assert shrink_towards_target_aspect_ratio(100, 10, 0.1, 1.0) == (10, 10)
    assert shrink_towards_target_aspect_ratio(200, 10, 0.1, 1.0) == (20, 10)

    # Shrink on columns only
    assert shrink_towards_target_aspect_ratio(10, 100, 0.1, 1.0) == (10, 10)
    assert shrink_towards_target_aspect_ratio(10, 200, 0.1, 1.0) == (10, 20)

    # Shrink on rows and columns and achieve target aspect ratio
    assert shrink_towards_target_aspect_ratio(100, 10, 0.1 / 4, 1.0) == (5, 5)
    assert shrink_towards_target_aspect_ratio(200, 10, 0.1 / 8, 1.0) == (5, 5)

    # Aspect ratio not one
    assert shrink_towards_target_aspect_ratio(100, 10, 0.1 / 2, 2.0) == (10, 5)
    assert shrink_towards_target_aspect_ratio(200, 10, 0.1 / 4, 2.0) == (10, 5)


@pytest.mark.parametrize("df", large_tables(N=10000, M=100))
@pytest.mark.parametrize("max_bytes", [1e3, 1e4, 1e5])
def test_df_with_many_rows_is_downsampled_preferentially_on_rows(df, max_bytes):
    dn, message = downsample(df, max_bytes=max_bytes)
    if max_bytes == 1e5:
        assert len(dn) == len(dn.columns) or (
            len(dn) < len(df) and len(dn.columns) == len(df.columns)
        )
    else:
        # aspect ratio is close to 1
        assert 0.5 < len(dn) / len(dn.columns) < 2


@pytest.mark.parametrize("df", large_tables(N=100, M=10000))
@pytest.mark.parametrize("max_bytes", [1e3, 1e4, 1e5])
def test_df_with_many_columns_is_downsampled_preferentially_on_columns(df, max_bytes):
    dn, message = downsample(df, max_bytes=max_bytes)
    if max_bytes == 1e5:
        assert len(dn) == len(dn.columns) or (
            len(dn) == len(df) and len(dn.columns) < len(df.columns)
        )
    else:
        # aspect ratio is close to 1
        assert 0.5 < len(dn) / len(dn.columns) < 2


def test_downsample_to_odd_number_of_rows():
    df = pd.DataFrame({"x": range(17)})
    dn, _ = downsample(df, max_rows=3)
    assert len(dn) == 3
    assert dn["x"].to_list() == [0, 1, 16]
