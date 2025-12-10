"""Compatibility layer for sample dataframes - imports from specialized modules"""

from typing import Any

try:
    import itables.sample_pandas_dfs as sample_pandas_dfs
except ImportError:
    sample_pandas_dfs = None

try:
    import itables.sample_polars_dfs as sample_polars_dfs
except ImportError:
    sample_polars_dfs = None


def get_countries(html: bool = False, climate_zone: bool = False) -> Any:
    """A Pandas DataFrame with the world countries (from the world bank data)
    Flags are loaded from https://flagpedia.net/"""
    if sample_pandas_dfs is not None:
        return sample_pandas_dfs.get_countries(html, climate_zone)
    if sample_polars_dfs is not None:
        return sample_polars_dfs.get_countries(html, climate_zone)
    raise ImportError("No supported dataframe library is available.")


def get_dict_of_test_dfs() -> dict[str, Any]:
    dfs = {}
    if sample_pandas_dfs is not None:
        dfs.update(sample_pandas_dfs.get_dict_of_test_dfs())
    if sample_polars_dfs is not None:
        dfs.update(sample_polars_dfs.get_dict_of_test_dfs())
    return dfs
