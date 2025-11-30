import subprocess
import warnings
from pathlib import Path

import pytest

try:
    import pandas as pd

    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False
    pytest.skip("Pandas is not available", allow_module_level=True)

from itables.downsample import downsample
from itables.shiny import DT

SHINY_APPS_PATH = Path(__file__).parent / ".." / "apps" / "shiny"
SHINY_APPS_PY_FILES = [
    f"{directory.name}/{file.stem}"
    for directory in SHINY_APPS_PATH.iterdir()
    if directory.is_dir()
    for file in directory.iterdir()
    if file.suffix == ".py"
]


def test_select_on_downsampled_df():
    """
    When a DF of 17 rows is downsampled to 3 rows,
    we can only select rows 0, 1, 16
    """
    df = pd.DataFrame({"x": range(17)})
    dn, _ = downsample(df, max_rows=3)
    assert len(dn) == 3

    with warnings.catch_warnings():
        warnings.simplefilter("error")
        DT(df, maxRows=3, selected_rows=[0, 1, 16])

    for row in [-1, 17]:
        with pytest.raises(IndexError, match="Selected rows out of range"):
            DT(df, maxRows=3, selected_rows=[row])

    for row in [2, 15]:
        with pytest.warns(match="no row with index between 2 and 15 can be selected"):
            DT(df, maxRows=3, selected_rows=[row])


pytest.importorskip("shiny")


@pytest.fixture(params=SHINY_APPS_PY_FILES)
def shiny_app(request) -> str:
    """Return the name of an example Shiny app"""
    return request.param


def test_shiny_apps_exist():
    assert (
        len(SHINY_APPS_PY_FILES) > 0
    ), "No Shiny apps found in the apps/shiny directory."


def test_shiny_apps_are_valid_python_scripts(
    shiny_app: str,
    ignore_errors=[
        "RuntimeError: express.ui.page_opts() can only "
        "be used inside of a standalone Shiny Express app"
    ],
):
    """Test that the Shiny apps are valid Python scripts.

    Note that we don't use importlib here, as importing
    shinywidgets causes an interaction with the widget tests
    """
    file_path = SHINY_APPS_PATH / f"{shiny_app}.py"
    result = subprocess.run(
        ["python", str(file_path)], capture_output=True, text=True, timeout=10
    )
    for error in ignore_errors:
        if error in result.stderr:
            pytest.xfail(error)
    assert result.returncode == 0, f"Process failed: {result.stderr}"


def test_table_id_in_DT():
    DT(df=None, table_id="my_table1")
