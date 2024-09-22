import runpy
from pathlib import Path

import pytest
from packaging.version import Version

try:
    from shiny import __version__ as shiny_version
except ImportError:
    shiny_version = "NA"


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
@pytest.mark.skipif(
    shiny_version == "NA" or Version(shiny_version) < Version("1.0"),
    reason=f"This test requires shiny>=1.0, got {shiny_version}",
)
def test_app_file(app_file):
    print(f"This is shiny=={shiny_version}")
    runpy.run_path(str(app_file))
