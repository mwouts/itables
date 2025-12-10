import pytest

try:
    from jupytext.cli import jupytext
except ImportError:
    jupytext = None
    pytest.skip("jupytext is not available", allow_module_level=True)

try:
    import pandas  # noqa F401
except ImportError:
    try:
        import polars  # noqa F401
    except ImportError:
        pytest.skip("Neither pandas nor polars is available", allow_module_level=True)
    else:
        lib = "polars"
else:
    lib = "pandas"


def text_notebook(connected, display_logo_when_loading=True):
    return f"""# %%
import itables

itables.options.display_logo_when_loading = {display_logo_when_loading}
itables.init_notebook_mode(connected={connected})

# %%
import {lib} as pd
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
    assert jupytext is not None
    jupytext([str(nb_py), "--to", "ipynb", "--set-kernel", "-", "--execute"])
    assert nb_ipynb.exists()
    if nb_ipynb.stat().st_size < (9000 if display_logo_when_loading else 5000):
        return
    raise AssertionError(
        f"Notebook size is too large: {nb_ipynb.stat().st_size} bytes:\n"
        f"{nb_ipynb.read_text()}"
    )


def test_offline_notebook_is_not_too_large(tmp_path):
    nb_py = tmp_path / "nb.py"
    nb_ipynb = tmp_path / "nb.ipynb"
    nb_py.write_text(text_notebook(connected=False))
    assert jupytext is not None
    jupytext([str(nb_py), "--to", "ipynb", "--set-kernel", "-", "--execute"])
    assert nb_ipynb.exists()
    size_in_kb = nb_ipynb.stat().st_size // 1024

    assert 850 < size_in_kb < 950
