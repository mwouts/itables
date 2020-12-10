"""Test that the code in all the test notebooks work, including README.md"""

import os

import jupytext
import pytest
from jupytext.cli import jupytext as jupytext_cli
from jupytext.cli import system


def tool_version(tool):
    try:
        args = tool.split(" ")
        args.append("--version")
        return system(*args)
    except (OSError, SystemExit):  # pragma: no cover
        return None


requires_nbconvert = pytest.mark.skipif(
    not tool_version("jupyter nbconvert"), reason="nbconvert not found"
)


def list_notebooks():
    """List the md notebooks in this package"""
    nb_path = os.path.dirname(os.path.abspath(__file__))
    notebooks = [
        os.path.join(nb_path, nb_file)
        for nb_file in os.listdir(nb_path)
        if nb_file.endswith(".md")
    ]

    assert notebooks
    return notebooks


@pytest.mark.parametrize("md_file", list_notebooks())
def test_run_notebooks(md_file):
    """Execute each notebook"""
    notebook = jupytext.read(md_file)
    context = {}
    for cell in notebook.cells:
        if cell.cell_type == "code" and not cell.source.startswith("%"):
            exec(cell.source, context)


@requires_nbconvert
def test_execute_readme_and_update_index_html():
    nb_path = os.path.dirname(os.path.abspath(__file__))
    readme = os.path.join(nb_path, "..", "README.md")
    index = os.path.join(nb_path, "..", "index.html")

    jupytext_cli([readme, "--execute", "--output", "README.ipynb"])
    system("jupyter", "nbconvert", "--to", "html", "README.ipynb")
    os.remove("README.ipynb")

    if not os.path.isfile(index):
        os.rename("README.html", index)
