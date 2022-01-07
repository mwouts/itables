import pandas as pd

from itables import init_notebook_mode


def test_init():
    assert not hasattr(pd.Series, "_repr_html_")

    init_notebook_mode(all_interactive=True)
    assert hasattr(pd.Series, "_repr_html_")

    init_notebook_mode(all_interactive=False)
    assert not hasattr(pd.Series, "_repr_html_")

    # No pb if we do this twice
    init_notebook_mode(all_interactive=False)
    assert not hasattr(pd.Series, "_repr_html_")
