import sys
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

pytestmark = pytest.mark.skipif(sys.version_info < (3, 8), reason="Require Python>=3.8")


def list_doc_notebooks():
    documentation_folder = Path(__file__).parent / ".." / "docs"
    for file in documentation_folder.iterdir():
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

    org_options = dir(opt)

    nb = jupytext.read(notebook)
    py_notebook = jupytext.writes(nb, "py:percent")
    exec(py_notebook, {})

    new_options = set(dir(opt)).difference(org_options)
    for name in new_options:
        delattr(opt, name)

    # Revert back to the non initialized mode
    init_notebook_mode(all_interactive=False, connected=True)
