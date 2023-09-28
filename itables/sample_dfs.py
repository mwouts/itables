import math
import string
from datetime import datetime, timedelta

try:
    from functools import lru_cache
except ImportError:
    from functools32 import lru_cache

from itertools import cycle

import numpy as np
import pandas as pd

try:
    import pytz
except ImportError:
    pytz = None

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

PANDAS_VERSION_MAJOR, PANDAS_VERSION_MINOR, _ = pd.__version__.split(".", 2)
PANDAS_VERSION_MAJOR = int(PANDAS_VERSION_MAJOR)
PANDAS_VERSION_MINOR = int(PANDAS_VERSION_MINOR)
if PANDAS_VERSION_MAJOR == 0:
    COLUMN_TYPES = [type for type in COLUMN_TYPES if type != "boolean"]
if PANDAS_VERSION_MAJOR == 2 and PANDAS_VERSION_MINOR == 1:
    # https://github.com/pandas-dev/pandas/issues/55080
    COLUMN_TYPES = [type for type in COLUMN_TYPES if type != "timedelta"]


def get_countries(html=True):
    """A Pandas DataFrame with the world countries (from the world bank data)
    Flags are loaded from https://flagpedia.net/"""
    df = pd.read_csv(find_package_file("samples/countries.csv"))
    df = df.rename(columns={"capitalCity": "capital", "name": "country"})
    df["iso2Code"] = df["iso2Code"].fillna("NA")  # Namibia
    df = df.set_index("iso2Code")[
        ["region", "country", "capital", "longitude", "latitude"]
    ].dropna()
    df.index.name = "code"

    if not html:
        return df

    df["flag"] = [
        '<a href="https://flagpedia.net/{code}">'
        '<img src="https://flagpedia.net/data/flags/h80/{code}.webp" '
        'alt="Flag of {country}"></a>'.format(code=code.lower(), country=country)
        for code, country in zip(df.index, df["country"])
    ]
    df["country"] = [
        '<a href="https://en.wikipedia.org/wiki/{}">{}</a>'.format(country, country)
        for country in df["country"]
    ]
    df["capital"] = [
        '<a href="https://en.wikipedia.org/wiki/{}">{}</a>'.format(capital, capital)
        for capital in df["capital"]
    ]
    return df


def get_population():
    """A Pandas Series with the world population (from the world bank data)"""
    return pd.read_csv(find_package_file("samples/population.csv")).set_index(
        "Country"
    )["SP.POP.TOTL"]


def get_indicators():
    """A Pandas DataFrame with a subset of the world bank indicators"""
    return pd.read_csv(find_package_file("samples/indicators.csv"))


def get_df_complex_index():
    df = get_countries()
    df = df.reset_index().set_index(["region", "country"])
    df.columns = pd.MultiIndex.from_arrays(
        [
            [
                "code"
                if col == "code"
                else "localisation"
                if col in ["longitude", "latitude"]
                else "data"
                for col in df.columns
            ],
            df.columns,
        ],
        names=["category", "detail"],
    )
    return df


def get_dict_of_test_dfs(N=100, M=100, polars=False):
    NM_values = np.reshape(np.linspace(start=0.0, stop=1.0, num=N * M), (N, M))

    test_dfs = {
        "empty": pd.DataFrame(dtype=float),
        "no_rows": pd.DataFrame(dtype=float, columns=["a"]),
        "no_columns": pd.DataFrame(dtype=float, index=["a"]),
        "no_rows_one_column": pd.DataFrame([1.0], index=["a"], columns=["a"]).iloc[:0],
        "no_columns_one_row": pd.DataFrame([1.0], index=["a"], columns=["a"]).iloc[
            :, :0
        ],
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
            dtype="bool" if PANDAS_VERSION_MAJOR == 0 else "boolean",
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
                        tzinfo=None if pytz is None else pytz.timezone("US/Eastern"),
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
        "countries": get_countries(),
        "capital": get_countries().set_index(["region", "country"])[["capital"]],
        "complex_index": get_df_complex_index(),
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
        "big_integers": pd.DataFrame(
            {
                "bigint": [
                    1234567890123456789,
                    2345678901234567890,
                    3456789012345678901,
                ],
                "expected": [
                    "1234567890123456789",
                    "2345678901234567890",
                    "3456789012345678901",
                ],
            }
        ),
    }

    if polars:
        import polars as pl
        import pyarrow as pa

        polars_dfs = {}
        for key in test_dfs:
            try:
                polars_dfs[key] = pl.from_pandas(test_dfs[key])
            except (pa.ArrowInvalid, ValueError):
                pass
        return polars_dfs

    return test_dfs


def get_dict_of_test_series(polars=False):
    series = {}
    for df_name, df in get_dict_of_test_dfs().items():
        if len(df.columns) > 6:
            continue
        for col in df.columns:
            # Case of duplicate columns
            if not isinstance(df[col], pd.Series):
                continue
            series["{}.{}".format(df_name, col)] = df[col]

    if polars:
        import polars as pl
        import pyarrow as pa

        polars_series = {}
        for key in series:
            try:
                polars_series[key] = pl.from_pandas(series[key])
            except (pa.ArrowInvalid, ValueError):
                pass

        # Add a Polar table with unsigned integers
        # https://github.com/mwouts/itables/issues/192
        polars_series["u32"] = (
            pl.DataFrame({"foo": [1, 1, 3, 1]}).groupby("foo").count()
        )

        return polars_series

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
        if PANDAS_VERSION_MAJOR >= 1:
            x.loc[np.random.binomial(n=1, p=0.1, size=rows) == 0] = pd.NA
        return x
    if type == "float":
        x = pd.Series(np.random.normal(size=rows), dtype=float)
        x.loc[np.random.binomial(n=1, p=0.05, size=rows) == 0] = float("nan")
        x.loc[np.random.binomial(n=1, p=0.05, size=rows) == 0] = float("inf")
        x.loc[np.random.binomial(n=1, p=0.05, size=rows) == 0] = float("-inf")
        return x
    if type == "str":
        return get_countries()["region"].sample(n=rows, replace=True)
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


def get_pandas_style():
    """This function returns the Pandas style object given as an example
    in the Pandas documentation:

    https://pandas.pydata.org/docs/user_guide/style.html#Styler-Object-and-HTML
    """
    df = pd.DataFrame(
        [[38.0, 2.0, 18.0, 22.0, 21, np.nan], [19, 439, 6, 452, 226, 232]],
        index=pd.Index(
            ["Tumour (Positive)", "Non-Tumour (Negative)"], name="Actual Label:"
        ),
        columns=pd.MultiIndex.from_product(
            [["Decision Tree", "Regression", "Random"], ["Tumour", "Non-Tumour"]],
            names=["Model:", "Predicted:"],
        ),
    )

    s = df.style.format("{:.0f}").hide(
        [("Random", "Tumour"), ("Random", "Non-Tumour")], axis="columns"
    )

    cell_hover = {  # for row hover use <tr> instead of <td>
        "selector": "td:hover",
        "props": [("background-color", "#ffffb3")],
    }
    index_names = {
        "selector": ".index_name",
        "props": "font-style: italic; color: darkgrey; font-weight:normal;",
    }
    headers = {
        "selector": "th:not(.index_name)",
        "props": "background-color: #000066; color: white;",
    }
    s.set_table_styles([cell_hover, index_names, headers])

    s.set_table_styles(
        [
            {"selector": "th.col_heading", "props": "text-align: center;"},
            {"selector": "th.col_heading.level0", "props": "font-size: 1.5em;"},
            {"selector": "td", "props": "text-align: center; font-weight: bold;"},
        ],
        overwrite=False,
    )

    s.set_table_styles(
        [  # create internal CSS classes
            {"selector": ".true", "props": "background-color: #e6ffe6;"},
            {"selector": ".false", "props": "background-color: #ffe6e6;"},
        ],
        overwrite=False,
    )

    cell_color = pd.DataFrame(
        [
            ["true ", "false ", "true ", "false "],
            ["false ", "true ", "false ", "true "],
        ],
        index=df.index,
        columns=df.columns[:4],
    )

    s.set_td_classes(cell_color)

    s.set_caption(
        "Confusion matrix for multiple cancer prediction models."
    ).set_table_styles(
        [{"selector": "caption", "props": "caption-side: bottom; font-size:1.25em;"}],
        overwrite=False,
    )

    tt = pd.DataFrame(
        [
            [
                "This model has a very strong true positive rate",
                "This model's total number of false negatives is too high",
            ]
        ],
        index=["Tumour (Positive)"],
        columns=df.columns[[0, 3]],
    )
    s.set_tooltips(
        tt,
        props="visibility: hidden; position: absolute; z-index: 1; border: 1px solid #000066;"
        "background-color: white; color: #000066; font-size: 0.8em;"
        "transform: translate(0px, -24px); padding: 0.6em; border-radius: 0.5em;",
    )

    s.set_table_styles(
        [  # create internal CSS classes
            {"selector": ".border-red", "props": "border: 2px dashed red;"},
            {"selector": ".border-green", "props": "border: 2px dashed green;"},
        ],
        overwrite=False,
    )

    cell_border = pd.DataFrame(
        [["border-green ", " ", " ", "border-red "], [" ", " ", " ", " "]],
        index=df.index,
        columns=df.columns[:4],
    )
    s.set_td_classes(cell_color + cell_border)

    return s
