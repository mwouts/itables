import os
import pytest
import jupytext
from nbconvert.preprocessors import ExecutePreprocessor


def list_notebooks():
    nb_path = os.path.dirname(os.path.abspath(__file__))
    notebooks = [os.path.join(nb_path, nb_file) for nb_file in os.listdir(nb_path) if nb_file.endswith('.md')]
    notebooks.append(os.path.join(nb_path, '..', 'README.md'))

    assert notebooks
    return notebooks


@pytest.mark.parametrize('md_file', list_notebooks())
def test_run_notebooks(md_file):
    nb = jupytext.readf(md_file)
    ep = ExecutePreprocessor(timeout=None, kernel_name='current_env')
    ep.preprocess(nb, {'metadata': {'path': os.path.dirname(os.path.abspath(__file__))}})
