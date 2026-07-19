"""Browser-based regression test for https://github.com/mwouts/itables/issues/426

VS Code's Jupyter extension sets the `data-vscode-theme-kind` attribute on
the <body> of the outer notebook webview, but renders ipywidget content
(such as itables' `ITable` widget) inside a same-origin iframe of its own.
Because of that, `document.body.dataset` as seen from within the widget's
own script never carries the attribute, and itables used to fall back to
the browser/OS `prefers-color-scheme`, which does not necessarily match
VS Code's theme -- so the table stayed light even in a dark-themed window.

This test reproduces that layout (an outer document with
`data-vscode-theme-kind`, and the itables output nested inside an iframe)
and checks that the table still picks up -- and stays in sync with -- the
theme exposed on the ancestor document.

It requires Playwright and its Chromium browser, which are not part of the
default test dependencies. Run it locally with the dedicated `playwright`
pixi environment, see docs/developing.md.
"""

import html as html_module

import pytest

pytest.importorskip("playwright")

try:
    import pandas as pd
except ImportError:
    pd = None
    pytest.skip("Pandas is not available", allow_module_level=True)

try:
    import IPython  # noqa: F401
except ImportError:
    pytest.skip("IPython is not available", allow_module_level=True)


from IPython.core.interactiveshell import InteractiveShell  # noqa: E402
from IPython.utils.capture import capture_output  # noqa: E402
from playwright.sync_api import (  # noqa: E402  # pyright: ignore[reportMissingImports]
    sync_playwright,
)


def render_widget_iframe_page() -> str:
    """Build a page that mimics VS Code's notebook layout: an outer document
    with `data-vscode-theme-kind` on its <body>, and the itables output
    nested inside a same-origin iframe (VS Code renders ipywidget content
    this way), by actually running the code through an IPython shell so
    that the `display()` calls made internally by itables are captured."""
    code = """
import pandas as pd
from IPython.display import HTML, display
from itables import init_notebook_mode, to_html_datatable

init_notebook_mode(all_interactive=False, connected=False)

df = pd.DataFrame({"name": ["a", "b", "c"]})
display(HTML(to_html_datatable(df, connected=False)))
"""
    shell = InteractiveShell.instance()
    with capture_output() as cap:
        result = shell.run_cell(code)
    result.raise_error()

    html_outputs = [
        out.data["text/html"] for out in cap.outputs if "text/html" in out.data
    ]
    inner_html = "<html><body>" + "\n".join(html_outputs) + "</body></html>"

    return (
        '<html><body data-vscode-theme-kind="vscode-light">'
        '<iframe id="widget-frame" srcdoc="'
        + html_module.escape(inner_html, quote=True)
        + '"></iframe>'
        "</body></html>"
    )


def test_widget_dark_class_follows_ancestor_theme(tmp_path):
    html_path = tmp_path / "table.html"
    html_path.write_text(render_widget_iframe_page(), encoding="utf-8")

    with sync_playwright() as p:
        browser = p.chromium.launch()
        try:
            page = browser.new_page(viewport={"width": 500, "height": 400})
            errors = []
            page.on("pageerror", lambda exc: errors.append(str(exc)))
            page.goto(html_path.as_uri())

            frame_element = page.wait_for_selector("#widget-frame")
            frame = frame_element.content_frame()
            assert frame is not None
            frame.wait_for_selector("table.dataTable")

            assert errors == []
            assert "dark" not in frame.evaluate("document.documentElement.className")

            # VS Code switches the outer webview to a dark theme, in place,
            # without reloading the page.
            page.evaluate("document.body.dataset.vscodeThemeKind = 'vscode-dark'")
            frame.wait_for_function(
                "document.documentElement.className.includes('dark')"
            )

            assert errors == []
            assert "dark" in frame.evaluate("document.documentElement.className")

            # And back to light.
            page.evaluate("document.body.dataset.vscodeThemeKind = 'vscode-light'")
            frame.wait_for_function(
                "!document.documentElement.className.includes('dark')"
            )

            assert errors == []
            assert "dark" not in frame.evaluate("document.documentElement.className")
        finally:
            browser.close()
