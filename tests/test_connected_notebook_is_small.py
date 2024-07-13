import pytest
from jupytext.cli import jupytext


def text_notebook(connected, display_logo_when_loading=True):
    return f"""# %%
from itables import init_notebook_mode
import itables.options as opt

opt.display_logo_when_loading = {display_logo_when_loading}
init_notebook_mode(all_interactive=True, connected={connected})

# %%
import pandas as pd
pd.DataFrame()
"""


@pytest.mark.parametrize("display_logo_when_loading", [True, False])
def test_connected_notebook_is_small(tmp_path, display_logo_when_loading):
    nb_py = tmp_path / "nb.py"
    nb_ipynb = tmp_path / "nb.ipynb"
    nb_py.write_text(
        text_notebook(
            connected=True, display_logo_when_loading=display_logo_when_loading
        )
    )
    jupytext([str(nb_py), "--to", "ipynb", "--set-kernel", "itables", "--execute"])
    assert nb_ipynb.exists()
    assert nb_ipynb.stat().st_size < (9000 if display_logo_when_loading else 5000)


def test_offline_notebook_is_not_too_large(tmp_path):
    nb_py = tmp_path / "nb.py"
    nb_ipynb = tmp_path / "nb.ipynb"
    nb_py.write_text(text_notebook(connected=False))
    jupytext([str(nb_py), "--to", "ipynb", "--set-kernel", "itables", "--execute"])
    assert nb_ipynb.exists()
    assert 700000 < nb_ipynb.stat().st_size < 800000
