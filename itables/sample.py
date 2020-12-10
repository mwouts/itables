"""A few sample data frames, useful for testing"""

import math
from datetime import datetime, timedelta

import numpy as np
import pandas as pd


def sample_dfs():
    """A list of dataframes with various dtypes"""
    return [
        pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]}),
        pd.DataFrame(
            {"a": [0, np.Infinity, np.NaN], "b": [-1.0, -np.Infinity, math.pi]}
        ),
        pd.DataFrame({"col.1": ["a", "b"], "col.2": ["c", "d"]}),
        pd.DataFrame({"a": [datetime(2000, 1, 1), datetime(2001, 1, 1)]}),
        pd.DataFrame({"a": [timedelta(days=2), timedelta(seconds=50)]}),
        pd.DataFrame({"obj": [{"a": 1}, {"b": 2, "c": 3}]}),
        pd.DataFrame(
            np.arange(16).reshape((4, 4)),
            columns=pd.MultiIndex.from_product((["A", "B"], [1, 2])),
            index=pd.MultiIndex.from_product((["C", "D"], [3, 4])),
        ),
    ]


def sample_series():
    """A list of series with various dtypes"""
    series = []
    for df in sample_dfs():
        for col in df:
            series.append(df[col])
    return series
