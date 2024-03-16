from jupytext.cli import jupytext


def text_notebook(connected):
    return """# %%
from itables import init_notebook_mode

init_notebook_mode(all_interactive=True, connected={})

# %%
import pandas as pd
pd.DataFrame()
""".format(
        connected
    )


def test_connected_notebook_is_small(tmp_path):
    nb_py = tmp_path / "nb.py"
    nb_ipynb = tmp_path / "nb.ipynb"
    nb_py.write_text(text_notebook(connected=True))
    jupytext([str(nb_py), "--to", "ipynb", "--set-kernel", "itables", "--execute"])
    assert nb_ipynb.exists()
    assert nb_ipynb.stat().st_size < 5000


def test_offline_notebook_is_not_too_large(tmp_path):
    nb_py = tmp_path / "nb.py"
    nb_ipynb = tmp_path / "nb.ipynb"
    nb_py.write_text(text_notebook(connected=False))
    jupytext([str(nb_py), "--to", "ipynb", "--set-kernel", "itables", "--execute"])
    assert nb_ipynb.exists()
    assert 700000 < nb_ipynb.stat().st_size < 800000
