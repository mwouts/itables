import math
import string
import sys
from datetime import datetime, timedelta

try:
    from functools import lru_cache
except ImportError:
    from functools32 import lru_cache

from itertools import cycle

import numpy as np
import pandas as pd
import pytz

from .utils import find_package_file

COLUMN_TYPES = [
    "bool",
    "int",
    "float",
    "str",
    "categories",
    "boolean",
    "Int64",
    "date",
    "datetime",
    "timedelta",
]

if sys.version_info < (3,):
    COLUMN_TYPES = [type for type in COLUMN_TYPES if type != "boolean"]


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
            dtype="boolean" if sys.version_info > (3,) else "bool",
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
                "datetime": [datetime(2000, 1, 1), datetime(2001, 1, 1), pd.NaT],
                "timestamp": [
                    pd.NaT,
                    datetime(2000, 1, 1, 18, 55, 33),
                    datetime(
                        2001,
                        1,
                        1,
                        18,
                        55,
                        55,
                        456654,
                        tzinfo=pytz.timezone("US/Eastern"),
                    ),
                ],
                "timedelta": [
                    timedelta(days=2),
                    timedelta(seconds=50),
                    pd.NaT - datetime(2000, 1, 1),
                ],
            }
        ),
        "date_range": pd.DataFrame(
            {"timestamps": pd.date_range("now", periods=5, freq="S")}
        ),
        "ordered_categories": pd.DataFrame(
            {"int": np.arange(4)},
            index=pd.CategoricalIndex(
                ["first", "second", "third", "fourth"],
                categories=["first", "second", "third", "fourth"],
                ordered=True,
                name="categorical_index",
            ),
        ),
        "ordered_categories_in_multiindex": pd.DataFrame(
            {"int": np.arange(4), "integer_index": np.arange(4)},
            index=pd.CategoricalIndex(
                ["first", "second", "third", "fourth"],
                categories=["first", "second", "third", "fourth"],
                ordered=True,
                name="categorical_index",
            ),
        ).set_index("integer_index", append=True),
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
            index=["row_{}".format(i) for i in range(N)],
            columns=["column_{}".format(j) for j in range(M)],
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
        "duplicated_columns": pd.DataFrame(
            np.arange(4, 8).reshape((2, 2)),
            columns=pd.Index(["A", "A"]),
            index=pd.MultiIndex.from_arrays(
                np.arange(4).reshape((2, 2)), names=["A", "A"]
            ),
        ),
        "named_column_index": pd.DataFrame({"a": [1]}).rename_axis("columns", axis=1),
    }


def get_dict_of_test_series():
    series = {}
    for df_name, df in get_dict_of_test_dfs().items():
        if len(df.columns) > 6:
            continue
        for col in df.columns:
            # Case of duplicate columns
            if not isinstance(df[col], pd.Series):
                continue
            series["{}.{}".format(df_name, col)] = df[col]
    return series


@lru_cache()
def generate_date_series():
    return pd.Series(pd.date_range("1677-09-23", "2262-04-10", freq="D"))


def generate_random_series(rows, type):
    if type == "bool":
        return pd.Series(np.random.binomial(n=1, p=0.5, size=rows), dtype=bool)
    if type == "boolean":
        x = generate_random_series(rows, "bool").astype(type)
        x.loc[np.random.binomial(n=1, p=0.1, size=rows) == 0] = pd.NA
        return x
    if type == "int":
        return pd.Series(np.random.geometric(p=0.1, size=rows), dtype=int)
    if type == "Int64":
        x = generate_random_series(rows, "int").astype(type)
        if sys.version_info >= (3,):
            x.loc[np.random.binomial(n=1, p=0.1, size=rows) == 0] = pd.NA
        return x
    if type == "float":
        x = pd.Series(np.random.normal(size=rows), dtype=float)
        x.loc[np.random.binomial(n=1, p=0.05, size=rows) == 0] = float("nan")
        x.loc[np.random.binomial(n=1, p=0.05, size=rows) == 0] = float("inf")
        x.loc[np.random.binomial(n=1, p=0.05, size=rows) == 0] = float("-inf")
        return x
    if type == "str":
        return get_countries()["name"].sample(n=rows, replace=True)
    if type == "categories":
        x = generate_random_series(rows, "str")
        return pd.Series(x, dtype="category")
    if type == "date":
        x = generate_date_series().sample(rows, replace=True)
        x.loc[np.random.binomial(n=1, p=0.1, size=rows) == 0] = pd.NaT
        return x
    if type == "datetime":
        x = generate_random_series(rows, "date") + np.random.uniform(
            0, 1, rows
        ) * pd.Timedelta(1, unit="D")
        return x
    if type == "timedelta":
        x = generate_random_series(rows, "datetime").sample(frac=1)
        return x.diff()
    raise NotImplementedError(type)


def generate_random_df(rows, columns, column_types=COLUMN_TYPES):
    rows = int(rows)
    types = np.random.choice(column_types, size=columns)
    columns = [
        "Column{}OfType{}".format(col, type.title()) for col, type in enumerate(types)
    ]

    series = {
        col: generate_random_series(rows, type) for col, type in zip(columns, types)
    }
    index = pd.Index(range(rows))
    for x in series.values():
        x.index = index

    return pd.DataFrame(series)
