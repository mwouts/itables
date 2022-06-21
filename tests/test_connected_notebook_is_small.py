from jupytext.cli import jupytext


def text_notebook(connected):
    return f"""# %%
from itables import init_notebook_mode

init_notebook_mode(all_interactive=True, connected={connected})

# %%
import pandas as pd
pd.DataFrame()
"""


def test_connected_notebook_is_small(tmp_path):
    nb_py = tmp_path / "nb.py"
    nb_ipynb = tmp_path / "nb.ipynb"
    nb_py.write_text(text_notebook(connected=True))
    jupytext([str(nb_py), "--to", "ipynb", "--set-kernel", "itables", "--execute"])
    assert nb_ipynb.exists()
    assert nb_ipynb.stat().st_size < 5_000


def test_offline_notebook_is_not_too_large(tmp_path):
    nb_py = tmp_path / "nb.py"
    nb_ipynb = tmp_path / "nb.ipynb"
    nb_py.write_text(text_notebook(connected=False))
    jupytext([str(nb_py), "--to", "ipynb", "--set-kernel", "itables", "--execute"])
    assert nb_ipynb.exists()
    assert 700_000 < nb_ipynb.stat().st_size < 750_000
