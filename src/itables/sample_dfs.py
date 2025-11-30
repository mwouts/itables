import math
import string
from datetime import datetime, timedelta
from functools import lru_cache
from itertools import cycle
from typing import Any, Sequence, cast

from .utils import find_package_file


def get_pandas_column_types() -> list[str]:
    """Return the list of column types available in the current Pandas version"""
    import pandas as pd

    column_types = [
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

    pd_version_major_str, pd_version_minor_str, _ = pd.__version__.split(".", 2)
    pandas_version_major = int(pd_version_major_str)
    pandas_version_minor = int(pd_version_minor_str)
    if pandas_version_minor == 0:
        column_types = [type for type in column_types if type != "boolean"]
    if pandas_version_major == 2 and pandas_version_minor == 1:
        # https://github.com/pandas-dev/pandas/issues/55080
        column_types = [type for type in column_types if type != "timedelta"]
    return column_types


def get_countries(html: bool = False, climate_zone: bool = False) -> "pd.DataFrame":
    """A Pandas DataFrame with the world countries (from the world bank data)
    Flags are loaded from https://flagpedia.net/"""
    import numpy as np
    import pandas as pd

    df = pd.read_csv(find_package_file("samples/countries.csv"))
    df = df.rename(columns={"capitalCity": "capital", "name": "country"})
    df["iso2Code"] = df["iso2Code"].fillna("NA")  # Namibia
    df = df.set_index("iso2Code")[
        ["region", "country", "capital", "longitude", "latitude"]
    ].dropna()
    df.index.name = "code"

    if html:
        df["flag"] = [
            '<a href="https://flagpedia.net/{code}">'
            '<img src="https://flagpedia.net/data/flags/h80/{code}.webp" '
            'alt="Flag of {country}"></a>'.format(
                code=cast(str, code).lower(), country=country
            )
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

    # Add columns for the searchPanes demo
    if climate_zone:
        df["climate_zone"] = np.where(
            df["latitude"].abs() < 23.43615,
            "Tropical",
            np.where(
                df["latitude"].abs() < 35,
                "Sub-tropical",
                # Artic circle is 66.563861 but there is no capital there => using 64
                np.where(df["latitude"].abs() < 64, "Temperate", "Frigid"),
            ),
        )
        df["hemisphere"] = np.where(df["latitude"] > 0, "North", "South")

    return df


def get_population() -> "pd.Series[float]":
    """A Pandas Series with the world population (from the world bank data)"""
    import pandas as pd

    return pd.read_csv(find_package_file("samples/population.csv")).set_index(
        "Country"
    )["SP.POP.TOTL"]


def get_indicators() -> "pd.DataFrame":
    """A Pandas DataFrame with a subset of the world bank indicators"""
    import pandas as pd

    return pd.read_csv(find_package_file("samples/indicators.csv"))


def get_df_complex_index() -> "pd.DataFrame":
    """A Pandas DataFrame with a complex index"""
    import pandas as pd

    df = get_countries()
    df = df.reset_index().set_index(["region", "country"])
    df.columns = pd.MultiIndex.from_arrays(
        [
            [
                (
                    "code"
                    if col == "code"
                    else "localisation" if col in ["longitude", "latitude"] else "data"
                )
                for col in df.columns
            ],
            df.columns,
        ],
        names=["category", "detail"],
    )
    return df


def get_dict_of_test_dfs(N: int = 100, M: int = 100) -> "dict[str, pd.DataFrame]":
    """A dictionary of Pandas DataFrames with various characteristics"""
    import numpy as np
    import pandas as pd

    try:
        import pytz
    except ImportError:
        pytz = None

    NM_values = np.reshape(np.linspace(start=0.0, stop=1.0, num=N * M), (N, M))

    return {
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
                "nan": [np.nan, -np.nan],
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
                    pd.NaT - datetime(2000, 1, 1),  # type: ignore
                ],
            }
        ),
        "date_range": pd.DataFrame(
            {"timestamps": pd.date_range("now", periods=5, freq="s")}
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
                np.arange(4).reshape((2, 2)), names=["A", "A"]  # type: ignore
            ),
        ),
        "named_column_index": pd.DataFrame({"a": [1]}).rename_axis("columns", axis=1),
        "big_integers": pd.DataFrame(
            {
                "bigint": [
                    -1234567890123456789,
                    1234567890123456789,
                    2345678901234567890,
                    3456789012345678901,
                ],
                "expected": [
                    "-1234567890123456789",
                    "1234567890123456789",
                    "2345678901234567890",
                    "3456789012345678901",
                ],
            }
        ),
    }


def get_dict_of_test_series() -> dict[str, Any]:
    """A dictionary of Pandas Series"""
    import pandas as pd

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


def get_dict_of_polars_test_dfs(N: int = 100, M: int = 100) -> dict[str, Any]:
    from datetime import datetime, timedelta

    import polars as pl

    # Create NM_values without numpy
    total_points = N * M
    NM_values = [[(i * N + j) / (total_points - 1) for j in range(M)] for i in range(N)]

    polars_dfs = {
        "empty": pl.DataFrame(),
        "no_rows": pl.DataFrame(schema={"a": pl.Float64}),
        "no_columns": pl.DataFrame(),
        "no_rows_one_column": pl.DataFrame([1.0], schema={"a": pl.Float64}).slice(0, 0),
        "no_columns_one_row": pl.DataFrame([1.0], schema={"a": pl.Float64}).select([]),
        "bool": pl.DataFrame(
            {
                "a": [True, True],
                "b": [True, False],
                "c": [False, True],
                "d": [False, False],
            }
        ),
        "nullable_boolean": pl.DataFrame(
            {
                "a": [True, True, None],
                "b": [True, False, False],
                "c": [False, None, True],
                "d": [None, False, False],
            },
            schema={"a": pl.Boolean, "b": pl.Boolean, "c": pl.Boolean, "d": pl.Boolean},
        ),
        "int": pl.DataFrame(
            {"a": [-1, 6], "b": [2, -7], "c": [-3, 8], "d": [4, -9], "e": [-5, 10]}
        ),
        "nullable_int": pl.DataFrame(
            {"a": [-1, 4, None], "b": [2, -5, 7], "c": [-3, 6, None]},
            schema={"a": pl.Int64, "b": pl.Int64, "c": pl.Int64},
        ),
        "float": pl.DataFrame(
            {
                "int": [0.0, 1.0],
                "inf": [float("inf"), float("-inf")],
                "nan": [float("nan"), float("nan")],
                "math": [math.pi, math.e],
            }
        ),
        "str": pl.DataFrame(
            {
                "text_column": ["some", "text"],
                "very_long_text_column": ["a " + "very " * 12 + "long text"] * 2,
            }
        ),
        "time": pl.DataFrame(
            {
                "datetime": [datetime(2000, 1, 1), datetime(2001, 1, 1), None],
                "timestamp": [
                    None,
                    datetime(2000, 1, 1, 18, 55, 33),
                    datetime(2001, 1, 1, 18, 55, 55, 456654),
                ],
                "timedelta": [timedelta(days=2), timedelta(seconds=50), None],
            }
        ),
        "date_range": pl.DataFrame(
            {
                "timestamps": pl.datetime_range(
                    datetime.now(),
                    datetime.now() + timedelta(seconds=4),
                    interval="1s",
                    eager=True,
                )
            }
        ),
        "ordered_categories": pl.DataFrame(
            {
                "int": range(4),
                "categorical_index": pl.Series(
                    ["first", "second", "third", "fourth"], dtype=pl.Categorical
                ),
            }
        ),
        "object": pl.DataFrame(
            {"dict": [{"a": 1}, {"b": 2, "c": 3}], "list": [["a"], [1, 2]]}
        ),
        "int_float_str": pl.DataFrame(
            {
                "int": range(N),
                "float": [5.0 - i * (5.0 / (N - 1)) for i in range(N)],
                "str": [
                    letter for letter, _ in zip(cycle(string.ascii_lowercase), range(N))
                ],
            }
        ),
        "wide": pl.DataFrame(
            {f"column_{j}": [NM_values[i][j] for i in range(N)] for j in range(M)}
        ),
        "long_column_names": pl.DataFrame(
            {
                "short name": [0] * 5,
                "very " * 5 + "long name": [0] * 5,
                "very " * 10 + "long name": [1] * 5,
                "very " * 20 + "long name": [2] * 5,
                "nospacein" + "very" * 50 + "longname": [3] * 5,
                "nospacein" + "very" * 100 + "longname": [3] * 5,
            }
        ),
        "big_integers": pl.DataFrame(
            {
                "bigint": [
                    -1234567890123456789,
                    1234567890123456789,
                    2345678901234567890,
                    3456789012345678901,
                ],
                "expected": [
                    "-1234567890123456789",
                    "1234567890123456789",
                    "2345678901234567890",
                    "3456789012345678901",
                ],
            }
        ),
        "countries": pl.read_csv(find_package_file("samples/countries.csv")),
        "population": pl.read_csv(find_package_file("samples/population.csv")),
        "capital": pl.read_csv(find_package_file("samples/countries.csv")).select(
            ["region", "country", "capital"]
        ),
    }

    return polars_dfs


def get_dict_of_polars_test_series() -> dict[str, Any]:
    """A dictionary of Polars Series"""
    import polars as pl
    import pyarrow as pa

    polars_series = {}
    series = get_dict_of_test_series()
    for key in series:
        try:
            polars_series[key] = pl.from_pandas(series[key])
        except (pa.ArrowInvalid, ValueError):
            pass

    # Add a Polar table with unsigned integers
    # https://github.com/mwouts/itables/issues/192
    # https://github.com/mwouts/itables/issues/299
    polars_series["u32"] = pl.Series([1, 2, 5]).cast(pl.UInt32)
    polars_series["u64"] = pl.Series([1, 2, 2**40]).cast(pl.UInt64)

    return polars_series


@lru_cache()
def generate_date_series():
    import pandas as pd

    if pd.__version__ >= "2.2.0":
        # https://github.com/pandas-dev/pandas/issues/55080 is back in 2.2.0?
        return pd.Series(pd.date_range("1970-01-01", "2099-12-31", freq="D"))
    return pd.Series(pd.date_range("1677-09-23", "2262-04-10", freq="D"))


def generate_random_series(rows: int, type: str) -> Any:
    """Generate a random Pandas Series of the given type and number of rows"""
    import numpy as np
    import pandas as pd

    if type == "bool":
        return pd.Series(np.random.binomial(n=1, p=0.5, size=rows), dtype=bool)
    if type == "boolean":
        x = generate_random_series(rows, "bool").astype(type)
        x.loc[np.random.binomial(n=1, p=0.1, size=rows) == 0] = pd.NA  # type: ignore
        return x
    if type == "int":
        return pd.Series(np.random.geometric(p=0.1, size=rows), dtype=int)
    if type == "Int64":
        x = generate_random_series(rows, "int").astype(type)
        x.loc[np.random.binomial(n=1, p=0.1, size=rows) == 0] = pd.NA  # type: ignore
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
        x.loc[np.random.binomial(n=1, p=0.1, size=rows) == 0] = pd.NaT  # type: ignore
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


def generate_random_df(
    rows: int, columns: int, column_types: Sequence[str] | None = None
) -> "pd.DataFrame":
    """Generate a random Pandas DataFrame with the given number of rows and columns
    and the given column types (if None, all available types are used)"""
    import numpy as np
    import pandas as pd

    if column_types is None:
        column_types = get_pandas_column_types()
    rows = int(rows)
    types = np.random.choice(column_types, size=columns)
    columns_names = [
        "Column{}OfType{}".format(col, type.title()) for col, type in enumerate(types)
    ]

    series = {
        col: generate_random_series(rows, type)
        for col, type in zip(columns_names, types)
    }
    index = pd.Index(range(rows))
    for x in series.values():
        x.index = index

    return pd.DataFrame(series)


def get_pandas_styler() -> Any:
    """This function returns a Pandas Styler object

    Cf. https://pandas.pydata.org/docs/user_guide/style.html
    """
    import numpy as np
    import pandas as pd

    x = np.linspace(0, math.pi, 21)
    df = pd.DataFrame(
        {"sin": np.sin(x), "cos": np.cos(x)}, index=pd.Index(x, name="alpha")
    )

    s = df.style
    s.background_gradient(axis=None, cmap="YlOrRd")
    s.format("{:.3f}")
    s.format_index("{:.3f}")

    s.set_caption(
        "A Pandas Styler object with background colors and tooltips"
    ).set_table_styles(
        [{"selector": "caption", "props": "caption-side: bottom; font-size:1.25em;"}],
    )

    ttips = pd.DataFrame(
        {
            "sin": ["The sinus of {:.6f} is {:.6f}".format(t, np.sin(t)) for t in x],
            "cos": ["The cosinus of {:.6f} is {:.6f}".format(t, np.cos(t)) for t in x],
        },
        index=df.index,
    )
    try:
        s.set_tooltips(ttips)
    except AttributeError:
        pass

    return s
