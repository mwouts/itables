import subprocess
import sys
from pathlib import Path

import jupytext
import pytest

import itables.options as opt
from itables import init_notebook_mode


def list_doc_notebooks():
    documentation_folder = Path(__file__).parent / ".." / "docs"
    for path in documentation_folder.iterdir():
        if path.suffix == ".md":
            yield path
        if path.is_dir():
            if path.name == ".ipynb_checkpoints":
                continue
            for file in path.iterdir():
                if file.suffix == ".md":
                    yield file


@pytest.mark.parametrize(
    "notebook", list_doc_notebooks(), ids=lambda notebook: notebook.stem
)
def test_run_documentation_notebooks(notebook):
    if ("polars" in notebook.stem or "formatting" in notebook.stem):
        pytest.importorskip("polars")
    if "pandas_style" in notebook.stem:
        pytest.importorskip("pandas.io.formats.style")
    if "marimo" in notebook.stem or "widget" in notebook.stem:
        pytest.importorskip("anywidget")

    nb = jupytext.read(notebook)
    py_notebook = jupytext.writes(nb, "py:percent")
    if "shiny" in notebook.stem:
        # we can't use exec as shinywidgets makes the widget.md notebook fail
        result = subprocess.run(
            [sys.executable, "-c", py_notebook], capture_output=True, text=True
        )
        if result.returncode != 0:
            if "ModuleNotFoundError: No module named 'shinywidgets'" in result.stderr:
                pytest.skip("shinywidgets is not available")
            assert result.returncode == 0, result.stderr
        return

    org_options = dir(opt)

    exec(py_notebook, {})

    new_options = set(dir(opt)).difference(org_options)
    for name in new_options:
        delattr(opt, name)

    # Revert back to the non initialized mode
    init_notebook_mode(all_interactive=False, connected=True)
