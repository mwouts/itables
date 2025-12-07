"""Sample Polars DataFrames and Series for testing and examples"""

import math
import string
from datetime import datetime, timedelta
from itertools import cycle

import polars as pl

from .utils import find_package_file


def get_countries(html: bool = False, climate_zone: bool = False) -> "pl.DataFrame":
    """A Polars DataFrame with the world countries (from the world bank data)
    Flags are loaded from https://flagpedia.net/"""
    df = pl.read_csv(find_package_file("samples/countries.csv"))
    df = df.rename({"capitalCity": "capital", "name": "country"})
    df = df.with_columns(pl.col("iso2Code").fill_null("NA"))  # Namibia
    df = df.filter(
        pl.col("region").is_not_null()
        & pl.col("country").is_not_null()
        & pl.col("capital").is_not_null()
        & pl.col("longitude").is_not_null()
        & pl.col("latitude").is_not_null()
    ).select(["iso2Code", "region", "country", "capital", "longitude", "latitude"])

    if html:
        df = df.with_columns(
            pl.struct(["iso2Code", "country"])
            .map_elements(
                lambda row: '<a href="https://flagpedia.net/{code}">'
                '<img src="https://flagpedia.net/data/flags/h80/{code}.webp" '
                'alt="Flag of {country}"></a>'.format(
                    code=row["iso2Code"].lower(), country=row["country"]
                ),
                return_dtype=pl.String,
            )
            .alias("flag")
        )
        df = df.with_columns(
            pl.col("country")
            .map_elements(
                lambda country: '<a href="https://en.wikipedia.org/wiki/{}">{}</a>'.format(
                    country, country
                ),
                return_dtype=pl.String,
            )
            .alias("country")
        )
        df = df.with_columns(
            pl.col("capital")
            .map_elements(
                lambda capital: '<a href="https://en.wikipedia.org/wiki/{}">{}</a>'.format(
                    capital, capital
                ),
                return_dtype=pl.String,
            )
            .alias("capital")
        )

    # Add columns for the searchPanes demo
    if climate_zone:
        df = df.with_columns(
            pl.when(pl.col("latitude").abs() < 23.43615)
            .then(pl.lit("Tropical"))
            .when(pl.col("latitude").abs() < 35)
            .then(pl.lit("Sub-tropical"))
            # Artic circle is 66.563861 but there is no capital there => using 64
            .when(pl.col("latitude").abs() < 64)
            .then(pl.lit("Temperate"))
            .otherwise(pl.lit("Frigid"))
            .alias("climate_zone")
        )
        df = df.with_columns(
            pl.when(pl.col("latitude") > 0)
            .then(pl.lit("North"))
            .otherwise(pl.lit("South"))
            .alias("hemisphere")
        )

    return df


def get_population() -> "pl.Series":
    """A Polars Series with the world population (from the world bank data)"""
    df = pl.read_csv(find_package_file("samples/population.csv"))
    return df.select(["Country", "SP.POP.TOTL"]).to_series(1)


def get_indicators() -> "pl.DataFrame":
    """A Polars DataFrame with a subset of the world bank indicators"""
    return pl.read_csv(find_package_file("samples/indicators.csv"))


def get_dict_of_test_dfs(N: int = 100, M: int = 100) -> "dict[str, pl.DataFrame]":
    """A dictionary of Polars DataFrames with various characteristics"""
    NM_values = [[(N * j + i) / (N * M) for j in range(M)] for i in range(N)]

    enum = pl.Enum(["first", "second", "third", "fourth"])

    return {
        "empty": pl.DataFrame(),
        "no_rows": pl.DataFrame(schema={"a": pl.Float64}),
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
            }
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
                "category": pl.Series(
                    ["first", "second", "third", "fourth"], dtype=enum
                ),
            }
        ),
        "object": pl.DataFrame(
            {"dict": [{"a": 1}, {"b": 2, "c": 3}], "list": [["a"], [1, 2]]}
        ),
        "countries": get_countries(),
        "int_float_str": pl.DataFrame(
            {
                "int": range(N),
                "float": [i + 0.5 for i in range(N)],
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
    }


def get_dict_of_test_series() -> "dict[str, pl.Series]":
    """A dictionary of Polars Series"""
    series = {}
    for df_name, df in get_dict_of_test_dfs().items():
        if len(df.columns) > 6:
            continue
        for col in df.columns:
            series[f"{df_name}.{col}"] = df[col]

    # Add Polars tables with unsigned integers
    # https://github.com/mwouts/itables/issues/192
    # https://github.com/mwouts/itables/issues/299
    series["u32"] = pl.Series([1, 2, 5], dtype=pl.UInt32)
    series["u64"] = pl.Series([1, 2, 2**40], dtype=pl.UInt64)

    return series
