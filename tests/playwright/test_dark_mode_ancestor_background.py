"""Browser-based regression test for https://github.com/mwouts/itables/issues/426

itables.org itself (built with Jupyter Book / pydata-sphinx-theme) showed the
same "controls are dark but the table isn't" symptom as the ITable widget,
even though it uses plain `to_html_datatable` output (no widget involved).

The cause: pydata-sphinx-theme paints a light "safety" background behind any
cell output that isn't a plain `table.dataframe`, so that outputs with
unknown/uncontrolled text color stay legible:

    html[data-theme="dark"] .bd-content div.cell_output
        .text_html:not(:has(table.dataframe)) { background-color: ...; }

Since itables renders `table.dataTable` (not `table.dataframe`), it is
caught by that rule. Because itables' own table cells are transparent by
design (they rely on the host's background showing through, see the
dark-mode fixed-columns fix for issue #564), that light ancestor background
showed through instead of a dark one.

This test reproduces the pattern generically (an ancestor with a hard-coded
light background, independent of the page's own dark-mode state) and checks
that `div.dt-container` now paints its own theme-aware background instead of
relying on transparency.

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


def render_offline_notebook_html() -> str:
    """Capture the HTML that itables would display in a notebook, wrapped in
    a page with a dark `data-theme` on <html> (so itables detects dark mode)
    but where the output itself sits inside an ancestor <div> with a
    hard-coded *light* background -- mimicking pydata-sphinx-theme's
    cell-output safety net -- by actually running the code through an
    IPython shell rather than calling the underlying functions directly, so
    that the `display()` calls made internally by itables are captured
    too."""
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
        '<html data-theme="dark"><body>'
        '<div class="cell_output" style="background-color: rgb(206, 214, 221);">'
        + "\n".join(html_outputs)
        + "</div></body></html>"
    )


def test_dt_container_background_wins_over_light_ancestor(tmp_path):
    html_path = tmp_path / "table.html"
    html_path.write_text(render_offline_notebook_html(), encoding="utf-8")

    with sync_playwright() as p:
        browser = p.chromium.launch()
        try:
            page = browser.new_page(viewport={"width": 500, "height": 400})
            errors = []
            page.on("pageerror", lambda exc: errors.append(str(exc)))
            page.goto(html_path.as_uri())
            page.wait_for_selector("table.dataTable")

            assert errors == []
            assert "dark" in page.evaluate("document.documentElement.className")

            container_background = page.evaluate(
                """
                () => getComputedStyle(
                  document.querySelector('div.dt-container')
                ).backgroundColor
                """
            )
            # itables' own dark background must win over the ancestor's
            # hard-coded light one.
            assert container_background == "rgb(33, 37, 41)"
        finally:
            browser.close()
