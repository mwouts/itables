import sys
from pathlib import Path

import pytest
from jupytext.cli import jupytext

pytestmark = pytest.mark.skipif(sys.version_info < (3,), reason="Not supported in Py2")


def list_doc_notebooks():
    documentation_folder = Path(__file__).parent / ".." / "docs"
    for file in documentation_folder.iterdir():
        if file.suffix == ".md":
            yield file


@pytest.mark.parametrize(
    "notebook", list_doc_notebooks(), ids=lambda notebook: notebook.stem
)
def test_documentation(notebook, tmp_path):
    notebook.hardlink_to(tmp_path / notebook.name)
    jupytext([str(tmp_path / notebook.name), "--set-kernel", "itables", "--execute"])
