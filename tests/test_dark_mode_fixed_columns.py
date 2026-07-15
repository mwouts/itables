"""Browser-based regression test for https://github.com/mwouts/itables/issues/564

This test renders a table with `fixedColumns` in a real (headless) browser and
checks that the fixed column gets the same dark background as the rest of the
table when dark mode is detected.

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
from playwright.sync_api import sync_playwright  # noqa: E402


def render_offline_notebook_html() -> str:
    """Capture the HTML that itables would display in a notebook, when
    a table with a fixed column needs horizontal scrolling. This mirrors
    what a real notebook (e.g. in VS Code) would produce, by actually
    running the code through an IPython shell rather than calling the
    underlying functions directly, so that the `display()` calls made
    internally by itables are captured too."""
    code = """
import pandas as pd
from IPython.display import HTML, display
from itables import init_notebook_mode, to_html_datatable

init_notebook_mode(all_interactive=False, connected=False)

df = pd.DataFrame(
    {
        "ticker": ["AAPL US", "NKE US"],
        **{f"col{i}": [583336.42, 55452.85] for i in range(20)},
    }
)
display(HTML(to_html_datatable(
    df,
    connected=False,
    scrollX=True,
    scrollCollapse=True,
    fixedColumns={"start": 1},
)))
"""
    shell = InteractiveShell.instance()
    with capture_output() as cap:
        result = shell.run_cell(code)
    result.raise_error()

    html_outputs = [
        out.data["text/html"] for out in cap.outputs if "text/html" in out.data
    ]
    # A dark background on the host page, mimicking a dark-themed notebook
    # front-end (e.g. VS Code): itables' regular cells are transparent by
    # design and rely on this to show through.
    return (
        "<html><head><style>body { background: #212529; }</style></head>"
        "<body>" + "\n".join(html_outputs) + "</body></html>"
    )


def test_fixed_column_background_matches_dark_mode(tmp_path):
    html_path = tmp_path / "table.html"
    html_path.write_text(render_offline_notebook_html(), encoding="utf-8")

    with sync_playwright() as p:
        browser = p.chromium.launch()
        try:
            page = browser.new_page(
                viewport={"width": 500, "height": 400}, color_scheme="dark"
            )
            errors = []
            page.on("pageerror", lambda exc: errors.append(str(exc)))
            page.goto(html_path.as_uri())
            page.wait_for_selector("td.dtfc-fixed-start")

            assert errors == []
            assert "dark" in page.evaluate("document.documentElement.className")

            fixed_background = page.evaluate(
                """
                () => getComputedStyle(
                  document.querySelector('td.dtfc-fixed-start')
                ).backgroundColor
                """
            )
            # The fixed column must use itables' dark background (issue #564:
            # the dark-mode detection script used to crash, so this stayed at
            # the light-mode default, rgb(255, 255, 255), even though the
            # rest of the table correctly turned dark).
            assert fixed_background == "rgb(33, 37, 41)"
        finally:
            browser.close()
