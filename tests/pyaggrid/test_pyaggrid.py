"""Test the pyaggrid package"""

import json
import re

import pyaggrid
import pyaggrid.options as opt
import pytest
from pyaggrid import JavascriptFunction, init_notebook_mode, to_html_aggrid
from pyaggrid.javascript import set_pyaggrid_repr_html_methods

pd = pytest.importorskip("pandas")


@pytest.fixture()
def df():
    return pd.DataFrame(
        {"a": [1, 2, 3], "b": [1.5, float("nan"), 3.25], "x": ["hello", "world", "!"]}
    )


def get_grid_args(html: str) -> dict:
    match = re.search(r"let grid_args = (\{.*?\});\n", html, flags=re.DOTALL)
    assert match is not None, html
    return json.loads(match.group(1))


def test_to_html_aggrid(df):
    html = to_html_aggrid(df, "my caption")
    assert "createGrid" in html
    grid_args = get_grid_args(html)
    assert grid_args["caption"] == "my caption"
    assert grid_args["columns"] == ["a", "b", "x"]
    data = json.loads(grid_args["data_json"])
    assert data[0] == [1, 1.5, "hello"]
    assert data[1][1] == "___NaN___"


def test_ag_grid_url_in_html(df):
    html = to_html_aggrid(df)
    assert opt.ag_grid_url in html


def test_downsampling_warning():
    big = pd.DataFrame({"a": range(10000)})
    html = to_html_aggrid(big, maxRows=20)
    grid_args = get_grid_args(html)
    assert "downsampled" in grid_args["downsampling_warning"]
    assert len(json.loads(grid_args["data_json"])) == 20


def test_named_index_is_shown():
    df = pd.DataFrame({"a": [1, 2]}, index=pd.Index(["x", "y"], name="idx"))
    grid_args = get_grid_args(to_html_aggrid(df))
    assert grid_args["columns"] == ["idx", "a"]


def test_trivial_index_is_not_shown(df):
    grid_args = get_grid_args(to_html_aggrid(df))
    assert grid_args["columns"] == ["a", "b", "x"]


def test_pagination_is_deactivated_on_small_tables(df):
    grid_args = get_grid_args(to_html_aggrid(df))
    assert "pagination" not in grid_args["grid_options"]

    big = pd.DataFrame({"a": range(100)})
    grid_args = get_grid_args(to_html_aggrid(big, maxBytes=0))
    assert grid_args["grid_options"]["pagination"] is True


def test_javascript_function_is_evaluated(df):
    html = to_html_aggrid(
        df, getRowStyle=JavascriptFunction("function (params) { return null; }")
    )
    grid_args = get_grid_args(html)
    assert grid_args["keys_to_be_evaluated"] == [["getRowStyle"]]


def test_table_id(df):
    html = to_html_aggrid(df, table_id="my_table")
    assert 'id="my_table"' in html

    with pytest.raises(ValueError, match="id name"):
        to_html_aggrid(df, table_id="0_starts_with_number")


def test_theme(df):
    grid_args = get_grid_args(to_html_aggrid(df, theme="balham"))
    assert grid_args["theme"] == "balham"


def test_undocumented_option_warns(df):
    with pytest.warns(SyntaxWarning, match="not documented"):
        to_html_aggrid(df, not_a_real_option=1)


def test_show(df):
    """show does not raise (outside of a notebook, IPython
    only prints the repr of the HTML object)"""
    pytest.importorskip("IPython")
    pyaggrid.show(df)


def test_init_notebook_mode(df):
    try:
        init_notebook_mode(all_interactive=True)
        assert "createGrid" in df._repr_html_()
    finally:
        set_pyaggrid_repr_html_methods(all_interactive=False)
    assert "createGrid" not in (df._repr_html_() or "")


def test_polars():
    pl = pytest.importorskip("polars")
    df = pl.DataFrame({"a": [1, 2], "b": ["x", "y"]})
    grid_args = get_grid_args(to_html_aggrid(df))
    assert grid_args["columns"] == ["a", "b"]
    assert json.loads(grid_args["data_json"]) == [[1, "x"], [2, "y"]]


def test_shared_core_with_pydatatables():
    """pyaggrid and pydatatables use the same core functions"""
    pytest.importorskip("pydatatables")
    import itables_core
    import pyaggrid.javascript
    import pydatatables.javascript

    assert (
        pyaggrid.javascript.downsample
        is pydatatables.javascript.downsample
        is itables_core.downsample.downsample
    )
    assert (
        pyaggrid.javascript.datatables_rows
        is pydatatables.javascript.datatables_rows
        is itables_core.formatting.datatables_rows
    )
