"""Test that the code in all the test notebooks work, including README.md"""

import pandas as pd
import pytest

from itables.downsample import downsample


def large_tables(N=1000, M=1000):
    return [
        pd.DataFrame(5, columns=range(M), index=range(N)),
        pd.DataFrame(3.14159, columns=range(M), index=range(N)),
        pd.DataFrame("abcdefg", columns=range(M), index=range(N)),
    ]


@pytest.mark.parametrize("df", large_tables())
@pytest.mark.parametrize("max_rows", [99, 100])
def test_max_rows(df, max_rows):
    dn = downsample(df, max_rows=max_rows)
    assert len(dn.index) == max_rows
    pd.testing.assert_index_equal(dn.columns, df.columns)


@pytest.mark.parametrize("df", large_tables())
@pytest.mark.parametrize("max_columns", [99, 100])
def test_max_columns(df, max_columns):
    dn = downsample(df, max_columns=max_columns)
    pd.testing.assert_index_equal(dn.index, df.index)
    assert len(dn.columns) == max_columns


@pytest.mark.parametrize("df", large_tables())
@pytest.mark.parametrize("max_bytes", [10, 1e2, 1e3, 1e4, 1e5])
def test_max_bytes(df, max_bytes):
    dn = downsample(df, max_bytes=max_bytes)
    assert dn.values.nbytes <= max_bytes
    assert dn.values.nbytes > max_bytes / 2


@pytest.mark.parametrize("df", large_tables())
def test_max_one_byte(df, max_bytes=1):
    dn = downsample(df, max_bytes=max_bytes)
    assert len(dn.columns) == len(dn.index) == 1
    assert dn.iloc[0, 0] == "..."


@pytest.mark.parametrize("df", large_tables(N=10000, M=100))
@pytest.mark.parametrize("max_bytes", [1e3, 1e4, 1e5])
def test_df_with_many_rows_is_downsampled_preferentially_on_rows(df, max_bytes):
    dn = downsample(df, max_bytes=max_bytes)
    if max_bytes == 1e5:
        assert len(dn.index) < len(df.index) and len(dn.columns) == len(df.columns)
    else:
        # aspect ratio is close to 1
        assert 0.5 < len(dn.index) / len(dn.columns) < 2


@pytest.mark.parametrize("df", large_tables(N=100, M=10000))
@pytest.mark.parametrize("max_bytes", [1e3, 1e4, 1e5])
def test_df_with_many_columns_is_downsampled_preferentially_on_columns(df, max_bytes):
    dn = downsample(df, max_bytes=max_bytes)
    if max_bytes == 1e5:
        assert len(dn.index) == len(df.index) and len(dn.columns) < len(df.columns)
    else:
        # aspect ratio is close to 1
        assert 0.5 < len(dn.index) / len(dn.columns) < 2
