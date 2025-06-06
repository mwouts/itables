from pathlib import Path

import jupytext
import pytest

import itables.options as opt
from itables import init_notebook_mode
from itables.javascript import pd_style

try:
    import polars as pl
except ImportError:
    pl = None


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
    if "polars" in notebook.stem and pl is None:
        pytest.skip("Polars is not available")
    if "pandas_style" in notebook.stem and pd_style is None:
        pytest.skip("Pandas Style is not available")
    if "shiny" in notebook.stem:
        pytest.skip("shinywidgets makes the widget.md notebook fail")
    if "marimo" in notebook.stem or "widget" in notebook.stem:
        pytest.importorskip("anywidget")

    org_options = dir(opt)

    nb = jupytext.read(notebook)
    py_notebook = jupytext.writes(nb, "py:percent")
    exec(py_notebook, {})

    new_options = set(dir(opt)).difference(org_options)
    for name in new_options:
        delattr(opt, name)

    # Revert back to the non initialized mode
    init_notebook_mode(all_interactive=False, connected=True)
