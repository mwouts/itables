import json

import pytest

from itables import show, to_html_datatable
from itables.datatables_format import _format_pandas_series, generate_encoder

try:
    import pandas as pd
except ImportError:
    pd = None
    pytest.skip("Pandas is not available", allow_module_level=True)
else:
    from itables.sample_pandas_dfs import (
        COLUMN_TYPES,
        generate_random_df,
        generate_random_series,
        get_countries,
        get_dict_of_test_dfs,
        get_dict_of_test_series,
        get_indicators,
        get_pandas_styler,
        get_population,
    )


try:
    import pandas.io.formats.style as pd_style
except ImportError:
    pd_style = None

try:
    import IPython  # noqa F401
except ImportError:
    show = to_html_datatable


# Make sure that displaying a dataframe does not trigger a warning  #107
pytestmark = [
    pytest.mark.filterwarnings("error"),
    # Seen on the CI on Py38 and Py39
    pytest.mark.filterwarnings("ignore::ResourceWarning"),
]


def test_get_countries(connected, use_to_html):
    df = get_countries(html=True)
    assert len(df.columns) > 5
    assert len(df.index) > 100
    show(df, connected=connected, use_to_html=use_to_html)


def test_get_population(connected, use_to_html):
    x = get_population()
    assert len(x) > 30
    assert x.max() > 7e9
    show(x, connected=connected, use_to_html=use_to_html)


def test_get_indicators(connected, use_to_html):
    df = get_indicators()
    assert len(df.index) == 500
    assert len(df.columns)
    show(df, connected=connected, use_to_html=use_to_html)


@pytest.mark.skipif(
    pd_style is None,
    reason="Missing optional dependency 'Jinja2'. DataFrame.style requires jinja2.",
)
def test_get_pandas_styler(connected):
    pytest.importorskip("matplotlib")
    styler = get_pandas_styler()
    show(styler, connected=connected, allow_html=True)


def kwargs_remove_none(**kwargs):
    return {key: value for key, value in kwargs.items() if value is not None}


def test_show_test_dfs(pd_df, connected, use_to_html, lengthMenu, monkeypatch):
    show(
        pd_df,
        connected=connected,
        use_to_html=use_to_html,
        **kwargs_remove_none(lengthMenu=lengthMenu),
    )


def test_to_html_datatable(pd_df, connected, use_to_html, lengthMenu, monkeypatch):
    to_html_datatable(
        pd_df,
        connected=connected,
        use_to_html=use_to_html,
        **kwargs_remove_none(lengthMenu=lengthMenu),
    )


def test_ordered_categories():
    df = get_dict_of_test_dfs()["ordered_categories"]
    assert df.index.is_monotonic_increasing
    assert df["int"].is_monotonic_increasing


@pytest.mark.parametrize("series_name,series", get_dict_of_test_series().items())
def test_format_pandas_series(
    series_name, series, escape_html, format_floats_in_python
):
    values = list(
        _format_pandas_series(
            series,
            escape_html=escape_html,
            format_floats_in_python=format_floats_in_python,
        )
    )
    json.dumps(values, cls=generate_encoder())


@pytest.mark.parametrize("series_name,series", get_dict_of_test_series().items())
def test_show_test_series(series_name, series, connected, use_to_html, monkeypatch):
    show(series, connected=connected, use_to_html=use_to_html)


def test_show_df_with_duplicate_column_names(connected, use_to_html):
    assert pd is not None
    df = pd.DataFrame({"a": [0], "b": [0.0], "c": ["str"]})
    df.columns = ["duplicated_name"] * 3
    show(df, connected=connected, use_to_html=use_to_html)


@pytest.mark.parametrize("type", COLUMN_TYPES)
def test_generate_random_series(type, rows=2000):
    assert pd is not None
    x = generate_random_series(rows, type)
    assert isinstance(x, pd.Series)
    assert len(x.index) == rows


def test_generate_random_df(rows=2000, cols=30):
    x = generate_random_df(rows, cols)
    assert len(x.index) == rows
    assert len(x.columns) == cols
