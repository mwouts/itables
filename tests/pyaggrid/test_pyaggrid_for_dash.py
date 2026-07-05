import pytest

pd = pytest.importorskip("pandas")
pytest.importorskip("dash")

from pyaggrid.dash import (  # noqa: E402
    AGGRID_PROPERTIES,
    AgGrid,
    PyAgGridOutputs,
    updated_aggrid_outputs,
)


@pytest.fixture()
def df():
    return pd.DataFrame({"a": [1, 2, 3], "x": ["u", "v", "w"]})


def test_aggrid_component(df):
    grid = AgGrid("my_grid", df, caption="hello")
    assert grid.id == "my_grid"
    assert grid.caption == "hello"
    assert "data_json" in grid.grid_args
    assert [
        col["headerName"] for col in grid.grid_args["grid_options"]["columnDefs"]
    ] == ["a", "x"]


def test_aggrid_component_requires_an_id(df):
    with pytest.raises(ValueError, match="id"):
        AgGrid("", df)


def test_aggrid_outputs():
    outputs = PyAgGridOutputs("my_grid")
    assert len(outputs) == len(AGGRID_PROPERTIES)


def test_updated_aggrid_outputs(df):
    updated = updated_aggrid_outputs(df, caption="x")
    assert len(updated) == len(AGGRID_PROPERTIES)


def test_updated_aggrid_outputs_preserves_data_when_df_is_none(df):
    grid = AgGrid("my_grid", df)
    updated = updated_aggrid_outputs(None, current_grid_args=grid.grid_args)
    grid_args = dict(zip(AGGRID_PROPERTIES, updated))["grid_args"]
    from dash import no_update

    assert grid_args is no_update
