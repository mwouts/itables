"""Browser-based regression test for https://github.com/mwouts/itables/issues/536

This test checks that itables' dark-mode detection respects Quarto's own
`quarto-light` / `quarto-dark` body class instead of falling back to the
browser/OS `prefers-color-scheme`, which does not necessarily match the
theme Quarto actually rendered the page in.

It requires Playwright and its Chromium browser, which are not part of the
default test dependencies. Run it locally with the dedicated `playwright`
pixi environment, see docs/developing.md.
"""

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


def render_offline_html(body_class: str) -> str:
    """Capture the HTML that itables would display in a notebook, and wrap
    it in a page that mimics a Quarto-rendered document (`<body
    class="quarto-light">` or `quarto-dark`), by actually running the code
    through an IPython shell rather than calling the underlying functions
    directly, so that the `display()` calls made internally by itables are
    captured too."""
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
    return (
        f'<html><body class="{body_class}">'
        + "\n".join(html_outputs)
        + "</body></html>"
    )


@pytest.mark.parametrize(
    "body_class, browser_color_scheme, expect_dark",
    [
        # Quarto rendered the page in its light theme: itables must stay
        # light even if the OS/browser prefers dark (issue #536 - a
        # light-themed Quarto page used to get the dark DataTables CSS,
        # making the ColumnControl icon and sort handles invisible, and the
        # search dropdown unreadable, because they were styled for a dark
        # background that was never actually there).
        ("quarto-light", "dark", False),
        # Quarto rendered the page in its dark theme: itables must follow,
        # even if the OS/browser prefers light.
        ("quarto-dark", "light", True),
    ],
)
def test_dark_class_follows_quarto_theme(
    tmp_path, body_class, browser_color_scheme, expect_dark
):
    html_path = tmp_path / "table.html"
    html_path.write_text(
        render_offline_html(body_class),
        encoding="utf-8",
    )

    with sync_playwright() as p:
        browser = p.chromium.launch()
        try:
            page = browser.new_page(
                viewport={"width": 500, "height": 400},
                color_scheme=browser_color_scheme,
            )
            errors = []
            page.on("pageerror", lambda exc: errors.append(str(exc)))
            page.goto(html_path.as_uri())
            page.wait_for_selector("table.dataTable")

            assert errors == []

            html_class = page.evaluate("document.documentElement.className")
            assert ("dark" in html_class) == expect_dark
        finally:
            browser.close()
