import importlib.util
from pathlib import Path

import pytest

STREAMLIT_APPS_PATH = Path(__file__).parent / ".." / "apps" / "streamlit"
STREAMLIT_APPS_PY_FILES = [
    file for file in STREAMLIT_APPS_PATH.iterdir() if file.suffix == ".py"
]

pytest.importorskip("streamlit")


@pytest.fixture(params=STREAMLIT_APPS_PY_FILES)
def streamlit_app(request) -> str:
    """Return the name of an example Streamlit app"""
    return request.param.stem


def test_streamlit_apps_exist():
    assert (
        len(STREAMLIT_APPS_PY_FILES) > 0
    ), "No Streamlit apps found in the apps/streamlit directory."


def test_streamlit_apps_can_be_imported(streamlit_app: str):
    """Test that the Streamlit apps can be imported successfully."""
    file_path = STREAMLIT_APPS_PATH / f"{streamlit_app}.py"
    spec = importlib.util.spec_from_file_location(streamlit_app, file_path)
    assert spec is not None, f"Could not find spec for {streamlit_app}"
    app = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(app)  # type: ignore
    assert app is not None
