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
    # The interactive HTML embeds a static, plain HTML fallback table in a
    # <noscript> tag - see #575
    html = pd.DataFrame({"x": [1]})._repr_html_()
    assert "<noscript>" in html
    assert ">1</td>" in html

    init_notebook_mode(all_interactive=False)
    assert not hasattr(pd.Series, "_repr_html_")

    # No pb if we do this twice
    init_notebook_mode(all_interactive=False)
    assert not hasattr(pd.Series, "_repr_html_")


def test_offline_dark_class_import_is_valid_js(monkeypatch):
    """The offline (connected=False) 'set_or_remove_dark_class' import must
    await the module namespace object exposed on window (a Promise), rather
    than passing that Promise to a second, invalid import() call.

    https://github.com/mwouts/itables/issues/564
    """
    displayed_html = []
    monkeypatch.setattr(
        "IPython.display.display", lambda x: displayed_html.append(x.data)
    )

    init_notebook_mode(all_interactive=False, connected=False)

    assert any("set_or_remove_dark_class" in html for html in displayed_html)
    for html in displayed_html:
        assert "await import(window." not in html
