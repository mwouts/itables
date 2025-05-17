import importlib.util
from pathlib import Path

import pytest

MARIMO_APPS_PATH = Path(__file__).parent / ".." / "apps" / "marimo"
MARIMO_APPS_PY_FILES = [
    file for file in MARIMO_APPS_PATH.iterdir() if file.suffix == ".py"
]

pytest.importorskip("marimo")


@pytest.fixture(params=MARIMO_APPS_PY_FILES)
def marimo_app(request) -> str:
    """Return the name of an example Marimo app"""
    return request.param.stem


def test_marimo_apps_exist():
    assert (
        len(MARIMO_APPS_PY_FILES) > 0
    ), "No Marimo apps found in the apps/marimo directory."


def test_marimo_apps_are_valid_python_scripts(marimo_app: str):
    """Test that the Marimo apps are valid Python scripts."""
    file_path = MARIMO_APPS_PATH / f"{marimo_app}.py"
    spec = importlib.util.spec_from_file_location(marimo_app, file_path)
    assert spec is not None, f"Could not find spec for {marimo_app}"
    app = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(app)  # type: ignore
    assert app is not None
