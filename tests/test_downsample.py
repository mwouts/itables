"""Test that the code in all the test notebooks work, including README.md"""

import itertools

import pandas as pd
import pytest

from itables.downsample import downsample


def large_tables(N=1000):
    return [
        pd.DataFrame(5, columns=range(N), index=range(N)),
        pd.DataFrame(3.14159, columns=range(N), index=range(N)),
        pd.DataFrame("abcdefg", columns=range(N), index=range(N)),
    ]


@pytest.mark.parametrize("df,max_rows", itertools.product(large_tables(), [99, 100]))
def test_max_rows(df, max_rows):
    dn = downsample(df, max_rows=max_rows)
    assert len(dn.index) == max_rows
    pd.testing.assert_index_equal(dn.columns, df.columns)


@pytest.mark.parametrize("df,max_columns", itertools.product(large_tables(), [99, 100]))
def test_max_columns(df, max_columns):
    dn = downsample(df, max_columns=max_columns)
    pd.testing.assert_index_equal(dn.index, df.index)
    assert len(dn.columns) == max_columns


@pytest.mark.parametrize(
    "df,max_bytes", itertools.product(large_tables(), [10, 1e2, 1e3, 1e4, 1e5])
)
def test_max_bytes(df, max_bytes):
    dn = downsample(df, max_bytes=max_bytes)
    assert dn.values.nbytes <= max_bytes
    assert dn.values.nbytes > max_bytes / 2


@pytest.mark.parametrize("df", large_tables())
def test_max_one_byte(df, max_bytes=1):
    dn = downsample(df, max_bytes=max_bytes)
    assert len(dn.columns) == len(dn.index) == 1
    assert dn.iloc[0, 0] == "..."
