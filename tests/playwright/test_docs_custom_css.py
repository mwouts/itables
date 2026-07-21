"""Browser-based regression test for https://github.com/mwouts/itables/issues/426

itables.org (built with Jupyter Book / pydata-sphinx-theme) shows the same
light-background-behind-a-dark-table symptom described in
test_dark_mode_ancestor_background.py, caused by pydata-sphinx-theme's own
dark-mode CSS:

    html[data-theme="dark"] .bd-content div.cell_output
        .text_html:not(:has(table.dataframe)) { background-color: ...; }

Since itables.org's pages only ever display itables' own output, which
never needs that safety net, docs/_static/custom.css neutralizes it
unconditionally (not just for outputs that happen to contain a
`table.dataTable` - some itables cells, like `init_notebook_mode()`, render
no visible table at all, yet were still getting the light background).

The theme's rule also sets a matching dark `color`, paired with its light
background. itables' own DataTable output (div.dt-container) sets its own
explicit color and so is unaffected either way, but the *static* fallback
table (shown when JS can't run) intentionally sets no color of its own -
so once the background half was neutralized, it inherited that dark color
on top of the page's own dark background instead, and became barely
readable. custom.css resets `color` to `inherit` too.

This test loads the real docs/_static/custom.css next to the theme's actual
selector (reproduced verbatim) and checks it wins - background, color and
padding - both when the output contains an itables table and when it
doesn't.

It requires Playwright and its Chromium browser, which are not part of the
default test dependencies. Run it locally with the dedicated `playwright`
pixi environment, see docs/developing.md.
"""

from pathlib import Path

import pytest

pytest.importorskip("playwright")

from playwright.sync_api import (  # noqa: E402  # pyright: ignore[reportMissingImports]
    sync_playwright,
)

CUSTOM_CSS = Path("docs/_static/custom.css").read_text(encoding="utf-8")

# Reproduced from pydata-sphinx-theme's own dark-mode CSS (see the comment
# in docs/_static/custom.css for context). The theme pairs its light safety
# background with a matching dark text color, meant to stay legible against
# that background - which becomes unreadable once only the background half
# is neutralized (issue #426 follow-up: the static fallback table, which
# sets no color of its own by design, inherited this dark color while
# sitting on the page's own dark background).
THEME_CSS = """
body { color: rgb(222, 226, 230); }
html[data-theme="dark"] .bd-content div.cell_output .text_html:not(:has(table.dataframe)) {
    background-color: rgb(206, 214, 221);
    color: rgb(33, 37, 41);
    border-radius: .25rem;
    padding: .5rem;
}
"""


@pytest.mark.parametrize(
    "inner_html",
    [
        pytest.param(
            '<table class="dataTable"><tbody><tr><td>1</td></tr></tbody></table>',
            id="with-table",
        ),
        pytest.param("<script>/* e.g. init_notebook_mode() */</script>", id="no-table"),
    ],
)
def test_custom_css_neutralizes_theme_safety_background(tmp_path, inner_html):
    html_path = tmp_path / "page.html"
    html_path.write_text(
        "<!DOCTYPE html>"
        '<html data-theme="dark"><head><style>'
        + THEME_CSS
        + CUSTOM_CSS
        + '</style></head><body><div class="bd-content"><div class="cell_output">'
        '<div class="text_html">' + inner_html + "</div>"
        "</div></div></body></html>",
        encoding="utf-8",
    )

    with sync_playwright() as p:
        browser = p.chromium.launch()
        try:
            page = browser.new_page(viewport={"width": 500, "height": 200})
            page.goto(html_path.as_uri())

            background = page.evaluate(
                "getComputedStyle(document.querySelector('.text_html')).backgroundColor"
            )
            padding = page.evaluate(
                "getComputedStyle(document.querySelector('.text_html')).paddingTop"
            )
            color = page.evaluate(
                "getComputedStyle(document.querySelector('.text_html')).color"
            )
            assert background == "rgba(0, 0, 0, 0)"
            assert padding == "0px"
            # Must inherit the page's own (light, readable) text color,
            # not the theme's dark one meant to pair with its light
            # background - otherwise content that sets no color of its
            # own (like the static fallback table) becomes unreadable.
            assert color == "rgb(222, 226, 230)"
        finally:
            browser.close()
