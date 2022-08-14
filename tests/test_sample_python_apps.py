import runpy
from pathlib import Path

import pytest


def get_app_file_list():
    return [
        app_file
        for app_file in (Path(__file__).parent / "sample_python_apps").iterdir()
    ]


def test_get_app_file_list():
    app_file_list = get_app_file_list()
    for app_file in app_file_list:
        assert app_file.suffix == ".py"
    assert "itables_in_a_shiny_app" in [app_file.stem for app_file in app_file_list]


@pytest.mark.parametrize("app_file", get_app_file_list(), ids=lambda path: path.stem)
def test_app_file(app_file):
    runpy.run_path(str(app_file))
