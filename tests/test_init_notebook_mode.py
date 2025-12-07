import pytest

try:
    import pandas as pd
except ImportError:
    pd = None
    pytest.skip("Pandas is not available", allow_module_level=True)

try:
    import IPython
except ImportError:
    IPython = None
    pytest.skip("IPython is not available", allow_module_level=True)


from itables import init_notebook_mode


def test_init_notebook_mode():
    assert pd is not None
    assert not hasattr(pd.Series, "_repr_html_")

    init_notebook_mode(all_interactive=True)
    assert hasattr(pd.Series, "_repr_html_")

    init_notebook_mode(all_interactive=False)
    assert not hasattr(pd.Series, "_repr_html_")

    # No pb if we do this twice
    init_notebook_mode(all_interactive=False)
    assert not hasattr(pd.Series, "_repr_html_")
