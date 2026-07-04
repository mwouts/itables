import importlib.util
import sys
from pathlib import Path

import pytest

STREAMLIT_APPS_PATH = Path(__file__).parent / ".." / ".." / "apps"
STREAMLIT_APPS_PY_FILES = [
    file for file in STREAMLIT_APPS_PATH.glob("*/streamlit/*.py")
]

pytest.importorskip("streamlit")


@pytest.fixture(params=STREAMLIT_APPS_PY_FILES)
def streamlit_app(request) -> str:
    """Return the name of an example Streamlit app"""
    return request.param.stem


def test_streamlit_apps_exist():
    assert (
        len(STREAMLIT_APPS_PY_FILES) > 0
    ), "No Streamlit apps found in the apps/*/streamlit directories."


def test_streamlit_apps_can_be_imported(streamlit_app: str):
    """Test that the Streamlit apps can be imported successfully."""
    if sys.version_info < (3, 10):
        pytest.skip("Streamlit v2 is not available on Python 3.9")

    (file_path,) = [f for f in STREAMLIT_APPS_PY_FILES if f.stem == streamlit_app]
    spec = importlib.util.spec_from_file_location(streamlit_app, file_path)
    assert spec is not None, f"Could not find spec for {streamlit_app}"
    app = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(app)  # type: ignore
    assert app is not None
