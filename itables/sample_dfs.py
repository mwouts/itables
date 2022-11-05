import math
import string
from datetime import datetime, timedelta
from itertools import cycle

import numpy as np
import pandas as pd

from .utils import find_package_file


def get_countries():
    """A Pandas DataFrame with the world countries (from the world bank data)"""
    return pd.read_csv(find_package_file("samples/countries.csv"))


def get_population():
    """A Pandas Series with the world population (from the world bank data)"""
    return pd.read_csv(find_package_file("samples/population.csv")).set_index(
        "Country"
    )["SP.POP.TOTL"]


def get_indicators():
    """A Pandas DataFrame with a subset of the world bank indicators"""
    return pd.read_csv(find_package_file("samples/indicators.csv"))


def get_dict_of_test_dfs(N=100, M=100):
    countries = get_countries()
    df_complex_index = countries.set_index(["region", "name"])
    df_complex_index.columns = (
        pd.DataFrame(
            {"category": ["code"] * 2 + ["property"] * 2 + ["localisation"] * 4},
            index=df_complex_index.columns.rename("detail"),
        )
        .set_index("category", append=True)
        .swaplevel()
        .index
    )

    NM_values = np.reshape(np.linspace(start=0.0, stop=1.0, num=N * M), (N, M))

    return {
        "empty": pd.DataFrame(),
        "bool": pd.DataFrame(
            [[True, True, False, False], [True, False, True, False]],
            columns=list("abcd"),
        ),
        "nullable_boolean": pd.DataFrame(
            [
                [True, True, False, None],
                [True, False, None, False],
                [None, False, True, False],
            ],
            columns=list("abcd"),
            dtype="boolean",
        ),
        "int": pd.DataFrame(
            [[-1, 2, -3, 4, -5], [6, -7, 8, -9, 10]], columns=list("abcde")
        ),
        "nullable_int": pd.DataFrame(
            [[-1, 2, -3], [4, -5, 6], [None, 7, None]],
            columns=list("abc"),
            dtype="Int64",
        ),
        "float": pd.DataFrame(
            {
                "int": [0.0, 1],
                "inf": [np.inf, -np.inf],
                "nan": [np.NaN, -np.NaN],
                "math": [math.pi, math.e],
            }
        ),
        "str": pd.DataFrame(
            {
                "text_column": ["some", "text"],
                "very_long_text_column": ["a " + "very " * 12 + "long text"] * 2,
            }
        ),
        "time": pd.DataFrame(
            {
                "datetime": [datetime(2000, 1, 1), datetime(2001, 1, 1)],
                "timedelta": [timedelta(days=2), timedelta(seconds=50)],
            }
        ),
        "date_range": pd.DataFrame(
            {"timestamps": pd.date_range("now", periods=5, freq="S")}
        ),
        "object": pd.DataFrame(
            {"dict": [{"a": 1}, {"b": 2, "c": 3}], "list": [["a"], [1, 2]]}
        ),
        "multiindex": pd.DataFrame(
            np.arange(16).reshape((4, 4)),
            columns=pd.MultiIndex.from_product((["A", "B"], [1, 2])),
            index=pd.MultiIndex.from_product((["C", "D"], [3, 4])),
        ),
        "countries": countries,
        "capital": countries.query('region!="Aggregates"').set_index(
            ["region", "name"]
        )[["capitalCity"]],
        "complex_index": df_complex_index,
        "int_float_str": pd.DataFrame(
            {
                "int": range(N),
                "float": np.linspace(5.0, 0.0, N),
                "str": [
                    letter for letter, _ in zip(cycle(string.ascii_lowercase), range(N))
                ],
            }
        ),
        "wide": pd.DataFrame(
            NM_values,
            index=[f"row_{i}" for i in range(N)],
            columns=[f"column_{j}" for j in range(M)],
        ),
        "long_column_names": pd.DataFrame(
            {
                "short name": [0] * 5,
                "very " * 5 + "long name": [0] * 5,
                "very " * 10 + "long name": [1] * 5,
                "very " * 20 + "long name": [2] * 5,
                "nospacein" + "very" * 50 + "longname": [3] * 5,
                "nospacein" + "very" * 100 + "longname": [3] * 5,
            }
        ),
        "sorted_index": pd.DataFrame(
            {"i": [0, 1, 2], "x": [0.0, 1.0, 2.0], "y": [0.0, 0.1, 0.2]}
        ).set_index(["i"]),
        "reverse_sorted_index": pd.DataFrame(
            {"i": [2, 1, 0], "x": [0.0, 1.0, 2.0], "y": [0.0, 0.1, 0.2]}
        ).set_index(["i"]),
        "sorted_multiindex": pd.DataFrame(
            {"i": [0, 1, 2], "j": [3, 4, 5], "x": [0.0, 1.0, 2.0], "y": [0.0, 0.1, 0.2]}
        ).set_index(["i", "j"]),
        "unsorted_index": pd.DataFrame(
            {"i": [0, 2, 1], "x": [0.0, 1.0, 2.0], "y": [0.0, 0.1, 0.2]}
        ).set_index(["i"]),
    }


def get_dict_of_test_series():
    series = {}
    for df_name, df in get_dict_of_test_dfs().items():
        if len(df.columns) > 6:
            continue
        for col in df.columns:
            series[f"{df_name}.{col}"] = df[col]
    return series
