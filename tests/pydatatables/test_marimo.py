import importlib.util
from pathlib import Path

import pytest

APPS_PATH = Path(__file__).parent / ".." / ".." / "apps"
MARIMO_APPS_PY_FILES = [
    file
    for marimo_dir in APPS_PATH.glob("*/marimo")
    for file in marimo_dir.iterdir()
    if file.suffix == ".py"
]

pytest.importorskip("marimo")


@pytest.fixture(params=MARIMO_APPS_PY_FILES)
def marimo_app(request) -> str:
    """Return the name of an example Marimo app"""
    return request.param.stem


def get_marimo_app_path(marimo_app: str):
    (file_path,) = [f for f in MARIMO_APPS_PY_FILES if f.stem == marimo_app]
    return file_path


def test_marimo_apps_exist():
    assert (
        len(MARIMO_APPS_PY_FILES) > 0
    ), "No Marimo apps found in the apps/*/marimo directories."


def test_marimo_apps_are_valid_python_scripts(marimo_app: str):
    """Test that the Marimo apps are valid Python scripts."""
    file_path = get_marimo_app_path(marimo_app)
    spec = importlib.util.spec_from_file_location(marimo_app, file_path)
    assert spec is not None, f"Could not find spec for {marimo_app}"
    app = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(app)  # type: ignore
    assert app is not None
