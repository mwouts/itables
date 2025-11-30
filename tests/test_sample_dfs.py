import json

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

from itables import show, to_html_datatable
from itables.datatables_format import generate_encoder

if PANDAS_AVAILABLE:
    from itables.datatables_format import _format_pandas_series
    from itables.sample_dfs import (
        generate_random_df,
        generate_random_series,
        get_countries,
        get_dict_of_test_dfs,
        get_dict_of_test_series,
        get_indicators,
        get_pandas_column_types,
        get_pandas_styler,
        get_population,
    )

if POLARS_AVAILABLE:
    from itables.datatables_format import _format_polars_series
    from itables.sample_dfs import get_dict_of_polars_test_series

# Make sure that displaying a dataframe does not trigger a warning  #107
pytestmark = [
    pytest.mark.filterwarnings("error"),
    # Seen on the CI on Py38 and Py39
    pytest.mark.filterwarnings("ignore::ResourceWarning"),
]

if PANDAS_AVAILABLE and int(pd.__version__.split(".")[0]) < 2:
    # DeprecationWarning: `cumproduct` is deprecated as of NumPy 1.25.0,
    # and will be removed in NumPy 2.0. Please use `cumprod` instead.
    pytestmark.append(pytest.mark.filterwarnings("ignore::DeprecationWarning"))


@pytest.mark.skipif(not PANDAS_AVAILABLE, reason="Pandas is not available")
def test_get_countries(connected, use_to_html):
    df = get_countries(html=True)
    assert len(df.columns) > 5
    assert len(df.index) > 100
    show(df, connected=connected, use_to_html=use_to_html)


@pytest.mark.skipif(not PANDAS_AVAILABLE, reason="Pandas is not available")
def test_get_population(connected, use_to_html):
    x = get_population()
    assert len(x) > 30
    assert x.max() > 7e9
    show(x, connected=connected, use_to_html=use_to_html)


@pytest.mark.skipif(not PANDAS_AVAILABLE, reason="Pandas is not available")
def test_get_indicators(connected, use_to_html):
    df = get_indicators()
    assert len(df.index) == 500
    assert len(df.columns)
    show(df, connected=connected, use_to_html=use_to_html)


def test_get_pandas_styler(connected):
    try:
        import pandas.io.formats.style
    except ImportError:
        pytest.skip("Pandas Style is not available")
    styler = get_pandas_styler()
    show(styler, connected=connected, allow_html=True)


def kwargs_remove_none(**kwargs):
    return {key: value for key, value in kwargs.items() if value is not None}


def test_show_test_dfs(df, connected, use_to_html, lengthMenu, monkeypatch):
    show(
        df,
        connected=connected,
        use_to_html=use_to_html,
        **kwargs_remove_none(lengthMenu=lengthMenu),
    )


def test_to_html_datatable(df, connected, use_to_html, lengthMenu, monkeypatch):
    to_html_datatable(
        df,
        connected=connected,
        use_to_html=use_to_html,
        **kwargs_remove_none(lengthMenu=lengthMenu),
    )


@pytest.mark.skipif(not PANDAS_AVAILABLE, reason="Pandas is not available")
def test_ordered_categories():
    df = get_dict_of_test_dfs()["ordered_categories"]
    assert df.index.is_monotonic_increasing
    assert df["int"].is_monotonic_increasing


@pytest.mark.skipif(not PANDAS_AVAILABLE, reason="Pandas is not available")
@pytest.mark.parametrize(
    "series_name,series",
    (
        [(name, series) for name, series in get_dict_of_test_series().items()]
        if PANDAS_AVAILABLE
        else []
    ),
)
def test_format_pandas_series(series_name, series):
    values = list(_format_pandas_series(series, escape_html=True))
    json.dumps(values, cls=generate_encoder())


@pytest.mark.skipif(not POLARS_AVAILABLE, reason="Polars is not available")
@pytest.mark.parametrize(
    "series_name,series",
    (
        [(name, series) for name, series in get_dict_of_polars_test_series().items()]
        if POLARS_AVAILABLE
        else []
    ),
)
def test_format_polars_series(series_name, series):
    values = list(_format_polars_series(series, escape_html=True))
    json.dumps(values, cls=generate_encoder())


@pytest.mark.skipif(not PANDAS_AVAILABLE, reason="Pandas is not available")
@pytest.mark.parametrize(
    "series_name,series",
    (
        [(name, series) for name, series in get_dict_of_test_series().items()]
        if PANDAS_AVAILABLE
        else []
    ),
)
def test_show_test_series(series_name, series, connected, use_to_html, monkeypatch):
    show(series, connected=connected, use_to_html=use_to_html)


@pytest.mark.skipif(not PANDAS_AVAILABLE, reason="Pandas is not available")
def test_show_df_with_duplicate_column_names(connected, use_to_html):
    df = pd.DataFrame({"a": [0], "b": [0.0], "c": ["str"]})
    df.columns = ["duplicated_name"] * 3
    show(df, connected=connected, use_to_html=use_to_html)


@pytest.mark.skipif(not PANDAS_AVAILABLE, reason="Pandas is not available")
@pytest.mark.parametrize("type", get_pandas_column_types() if PANDAS_AVAILABLE else [])
def test_generate_random_series(type, rows=2000):
    x = generate_random_series(rows, type)
    assert isinstance(x, pd.Series)
    assert len(x.index) == rows


@pytest.mark.skipif(not PANDAS_AVAILABLE, reason="Pandas is not available")
def test_generate_random_df(rows=2000, cols=30):
    x = generate_random_df(rows, cols)
    assert len(x.index) == rows
    assert len(x.columns) == cols
