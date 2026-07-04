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


def get_grid_options(html: str) -> dict:
    match = re.search(r"let gridOptions = (\{.*?\});\n", html, flags=re.DOTALL)
    assert match is not None, html
    return json.loads(match.group(1))


def get_data(html: str) -> list:
    match = re.search(r"let data = (\[.*?\]);\n", html, flags=re.DOTALL)
    assert match is not None, html
    return json.loads(match.group(1))


def get_header_names(html: str) -> list:
    return [col["headerName"] for col in get_grid_options(html)["columnDefs"]]


def test_to_html_aggrid(df):
    html = to_html_aggrid(df, "my caption")
    assert "createGrid" in html
    assert ">my caption</div>" in html
    assert get_header_names(html) == ["a", "b", "x"]
    data = get_data(html)
    assert data[0] == [1, 1.5, "hello"]
    assert data[1][1] == "___NaN___"


def test_column_defs(df):
    column_defs = get_grid_options(to_html_aggrid(df))["columnDefs"]
    assert column_defs[0]["field"] == "c0"
    # numeric columns are right-aligned and get a number filter
    assert column_defs[0]["type"] == "rightAligned"
    assert column_defs[1]["filter"] == "agNumberColumnFilter"
    assert "type" not in column_defs[2]


def test_ag_grid_url_in_html(df):
    html = to_html_aggrid(df)
    assert opt.ag_grid_url in html


def test_downsampling_warning():
    big = pd.DataFrame({"a": range(10000)})
    html = to_html_aggrid(big, maxRows=20)
    assert "pyaggrid-downsampling-warning" in html
    assert "downsampled" in html
    assert len(get_data(html)) == 20


def test_no_downsampling_warning_on_small_tables(df):
    html = to_html_aggrid(df)
    assert "pyaggrid-downsampling-warning" not in html


def test_named_index_is_shown():
    df = pd.DataFrame({"a": [1, 2]}, index=pd.Index(["x", "y"], name="idx"))
    assert get_header_names(to_html_aggrid(df)) == ["idx", "a"]


def test_trivial_index_is_not_shown(df):
    assert get_header_names(to_html_aggrid(df)) == ["a", "b", "x"]


def test_pagination_is_deactivated_on_small_tables(df):
    grid_options = get_grid_options(to_html_aggrid(df))
    assert "pagination" not in grid_options

    big = pd.DataFrame({"a": range(100)})
    grid_options = get_grid_options(to_html_aggrid(big, maxBytes=0))
    assert grid_options["pagination"] is True


def test_javascript_function_is_evaluated(df):
    html = to_html_aggrid(
        df, getRowStyle=JavascriptFunction("function (params) { return null; }")
    )
    grid_options = get_grid_options(html)
    assert grid_options["keys_to_be_evaluated"] == [["getRowStyle"]]


def test_script_content_is_escaped():
    df = pd.DataFrame({"a": ["</script>"]})
    html = to_html_aggrid(df)
    # in the raw HTML the cell value is escaped, so only the template's
    # own closing tag appears; the JSON escape resolves back to the value
    assert html.count("</script>") == 1
    assert get_data(html) == [["</script>"]]


def test_table_id(df):
    html = to_html_aggrid(df, table_id="my_table")
    assert 'id="my_table"' in html

    with pytest.raises(ValueError, match="id name"):
        to_html_aggrid(df, table_id="0_starts_with_number")


def test_theme(df):
    grid_options = get_grid_options(to_html_aggrid(df, theme="balham"))
    assert grid_options["theme"] == "balham"


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
    html = to_html_aggrid(df)
    assert get_header_names(html) == ["a", "b"]
    assert get_data(html) == [[1, "x"], [2, "y"]]
    # the numeric column is right aligned
    assert get_grid_options(html)["columnDefs"][0]["type"] == "rightAligned"


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
