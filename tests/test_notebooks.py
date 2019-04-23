"""Test that the code in all the test notebooks work, including README.md"""

import os
import pytest
import jupytext


def list_notebooks():
    """List the md notebooks in this package"""
    nb_path = os.path.dirname(os.path.abspath(__file__))
    notebooks = [os.path.join(nb_path, nb_file) for nb_file in os.listdir(nb_path) if nb_file.endswith('.md')]
    notebooks.append(os.path.join(nb_path, '..', 'README.md'))

    assert notebooks
    return notebooks


@pytest.mark.parametrize('md_file', list_notebooks())
def test_run_notebooks(md_file):
    """Execute each notebook"""
    notebook = jupytext.readf(md_file)
    context = {}
    for cell in notebook.cells:
        if cell.cell_type == 'code' and not cell.source.startswith('%'):
            exec(cell.source, context)
