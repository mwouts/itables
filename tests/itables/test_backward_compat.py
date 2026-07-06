"""Test that the historical itables API still works through the pydatatables wrapper"""

from importlib.util import find_spec

import pytest

import itables

pd = pytest.importorskip("pandas")


@pytest.fixture()
def df():
    return pd.DataFrame({"a": [1, 2, 3], "x": ["hello", "world", "!"]})


def test_version():
    assert itables.__version__.startswith("3.")


def test_to_html_datatable(df):
    html = itables.to_html_datatable(df)
    assert "new DataTable" in html
    assert "hello" in html


def test_show(df):
    """show does not raise (outside of a notebook, IPython
    only prints the repr of the HTML object)"""
    pytest.importorskip("IPython")
    itables.show(df)


def test_init_notebook_mode(df):
    from itables.javascript import set_itables_repr_html_methods

    try:
        itables.init_notebook_mode(all_interactive=True, connected=True)
        assert "new DataTable" in df._repr_html_()
    finally:
        set_itables_repr_html_methods(all_interactive=False)


def test_options_is_pydatatables_options():
    import itables.options as opt
    import pydatatables.options as pydatatables_opt

    assert opt is pydatatables_opt

    saved = opt.maxBytes
    try:
        opt.maxBytes = "32KB"
        assert pydatatables_opt.maxBytes == "32KB"
    finally:
        opt.maxBytes = saved


def test_options_are_used(df):
    import itables.options as opt

    saved = opt.maxRows

    try:
        opt.maxRows = 2
        html = itables.to_html_datatable(df, maxBytes=0)
        assert "downsampled" in html
    finally:
        opt.maxRows = saved


def test_typing_aliases():
    from itables.typing import DataFrameOrSeries  # noqa: F401
    from itables.typing import JavascriptCode  # noqa: F401
    from itables.typing import JavascriptFunction  # noqa: F401
    from itables.typing import (
        DTForITablesOptions,
        ITableOptions,
    )
    from pydatatables.typing import (
        PyDataTablesOptions,
        PyDataTablesRendererOptions,
    )

    assert ITableOptions is PyDataTablesOptions
    assert DTForITablesOptions is PyDataTablesRendererOptions


def test_downsample_module():
    import itables_core.downsample
    from itables.downsample import as_nbytes, downsample, nbytes  # noqa: F401

    assert downsample is itables_core.downsample.downsample


def test_datatables_format_module():
    from itables.datatables_format import datatables_rows  # noqa: F401


def test_sample_dfs():
    from itables.sample_dfs import get_countries, get_dict_of_test_dfs  # noqa: F401

    assert "int" in get_dict_of_test_dfs()


def test_javascript_aliases():
    from itables.javascript import generate_init_offline_itables_html  # noqa: F401
    from itables.javascript import to_html_datatable  # noqa: F401
    from itables.javascript import (
        get_itables_extension_arguments,
    )
    from pydatatables.javascript import get_pydatatables_extension_arguments

    assert get_itables_extension_arguments is get_pydatatables_extension_arguments


def test_get_itables_extension_arguments(df):
    from itables.javascript import get_itables_extension_arguments

    dt_args, other_args = get_itables_extension_arguments(df)
    assert "data_json" in dt_args
    assert "classes" in other_args


def test_config_module():
    from itables.config import get_config_file, load_config_file  # noqa: F401


@pytest.mark.skipif(find_spec("anywidget") is None, reason="anywidget is not available")
def test_widget(df):
    from pydatatables.widget import DataTable

    from itables.widget import ITable

    assert ITable is DataTable
    widget = ITable(df)
    assert widget.selected_rows == []


@pytest.mark.skipif(find_spec("dash") is None, reason="dash is not available")
def test_dash():
    from itables.dash import ITABLE_PROPERTIES, ITable, ITableOutputs  # noqa: F401
    from pydatatables.dash import DataTable, PyDataTablesRendererOutputs

    assert ITable is DataTable
    assert ITableOutputs is PyDataTablesRendererOutputs


@pytest.mark.skipif(find_spec("streamlit") is None, reason="streamlit is not available")
def test_streamlit():
    pytest.importorskip("streamlit.components.v2")
    from itables.streamlit import interactive_table
    from pydatatables.streamlit import datatable

    assert interactive_table is datatable


@pytest.mark.skipif(find_spec("shiny") is None, reason="shiny is not available")
def test_shiny(df):
    from itables.shiny import DT, init_itables  # noqa: F401

    html = DT(df)
    assert "new DataTable" in html
