"""Browser-based regression test for https://github.com/mwouts/itables/issues/536

This test renders a table with a `columnControl` search dropdown in a real
(headless) browser and checks that the dropdown does not include the stray,
unstyled search icon that broke its layout (the icon/select misalignment, and
completely broken date picker, reported in the issue).

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


def render_offline_html() -> str:
    """Capture the HTML that itables would display in a notebook, for a
    table with a columnControl search dropdown, by actually running the code
    through an IPython shell rather than calling the underlying functions
    directly, so that the `display()` calls made internally by itables are
    captured too."""
    code = """
import pandas as pd
from IPython.display import HTML, display
from itables import init_notebook_mode, to_html_datatable

init_notebook_mode(all_interactive=False, connected=False)

df = pd.DataFrame({"name": ["a", "b", "c"]})
display(HTML(to_html_datatable(
    df,
    connected=False,
    columnControl={"target": 0, "content": ["searchDropdown"]},
)))
"""
    shell = InteractiveShell.instance()
    with capture_output() as cap:
        result = shell.run_cell(code)
    result.raise_error()

    html_outputs = [
        out.data["text/html"] for out in cap.outputs if "text/html" in out.data
    ]
    return "<html><body>" + "\n".join(html_outputs) + "</body></html>"


def test_column_control_search_dropdown_has_no_stray_icon(tmp_path):
    html_path = tmp_path / "table.html"
    html_path.write_text(render_offline_html(), encoding="utf-8")

    with sync_playwright() as p:
        browser = p.chromium.launch()
        try:
            page = browser.new_page(viewport={"width": 500, "height": 400})
            errors = []
            page.on("pageerror", lambda exc: errors.append(str(exc)))
            page.goto(html_path.as_uri())
            page.wait_for_selector("span.dtcc button.dtcc-button")
            page.click("span.dtcc button.dtcc-button")
            page.wait_for_selector("div.dtcc-dropdown")

            assert errors == []

            # The dropdown's search box ships with an extra, unstyled search
            # icon (div.dtcc-search-icon) that only the inline (column
            # header) search box hides. Left visible in the dropdown, it
            # falls into the flex layout as an extra row, pushing the type
            # icon and the select apart and breaking the search/date-picker
            # controls below it (issue #536).
            icon_display = page.evaluate(
                """
                () => getComputedStyle(
                  document.querySelector('div.dtcc-dropdown div.dtcc-search-icon')
                ).display
                """
            )
            assert icon_display == "none"
        finally:
            browser.close()
