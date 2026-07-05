import pyaggrid.options as opt
import pytest

pd = pytest.importorskip("pandas")
pytest.importorskip("anywidget")


@pytest.fixture()
def df():
    return pd.DataFrame({"a": [1, 2, 3], "x": ["u", "v", "w"]})


def test_create_widget_with_no_df():
    from pyaggrid.widget import AgGrid

    grid = AgGrid()
    assert grid._df is None
    assert grid.caption == ""
    assert grid.classes == opt.classes
    assert grid.style == opt.style
    assert grid.selected_rows == []
    assert grid._grid_args["data_json"] == "[]"


def test_create_widget_with_df(df):
    from pyaggrid.widget import AgGrid

    grid = AgGrid(df, "the caption", selected_rows=[1])
    assert grid.df is df
    assert grid.caption == "the caption"
    assert grid.selected_rows == [1]
    grid_options = grid._grid_args["grid_options"]
    assert [col["headerName"] for col in grid_options["columnDefs"]] == ["a", "x"]
    assert grid._grid_args["data_json"].startswith("[[1,")


def test_update_widget(df):
    from pyaggrid.widget import AgGrid

    grid = AgGrid(df)
    grid.update(caption="new caption", theme="balham")
    assert grid.caption == "new caption"
    assert grid._grid_args["grid_options"]["theme"] == "balham"
    # the data is preserved when df is not passed
    assert grid._grid_args["data_json"].startswith("[[1,")

    df2 = pd.DataFrame({"b": [4.5, 5.5]})
    grid.df = df2
    assert grid.df is df2
    assert grid._grid_args["data_json"].startswith("[[4.5]")


def test_selected_rows_are_filtered_on_downsampled_tables():
    from pyaggrid.widget import AgGrid

    df = pd.DataFrame({"a": range(100)})
    with pytest.warns(UserWarning, match="downsampled"):
        grid = AgGrid(df, maxRows=10, selected_rows=[0, 50, 99])
    assert grid.selected_rows == [0, 99]


def test_ag_grid_url_is_rejected(df):
    from pyaggrid.widget import AgGrid

    with pytest.raises(TypeError, match="ag_grid_url"):
        AgGrid(df, ag_grid_url="https://example.com/aggrid.js")
