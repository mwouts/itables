"""Browser-based regression test for https://github.com/mwouts/itables/issues/576

This test checks that itables keeps the 'dark' class on <html> in sync when
the host (Jupyter Lab or VS Code) theme changes *after* the table has already
been rendered, instead of only detecting the theme once at init time.

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


def render_offline_notebook_html(body_dataset_attrs: str) -> str:
    """Capture the HTML that itables would display in a notebook, wrapped in
    a page that starts with the given data-attributes on <body> (mimicking
    e.g. VS Code's initial 'light' theme), by actually running the code
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
        f"<html><body {body_dataset_attrs}>"
        + "\n".join(html_outputs)
        + "</body></html>"
    )


@pytest.mark.parametrize(
    "host, initial_attrs, switch_to_dark_js, switch_to_light_js",
    [
        # VS Code sets this data-attribute on <body>, and updates it live
        # (without reloading the page) when the user switches theme.
        (
            "vscode",
            'data-vscode-theme-kind="vscode-light"',
            "document.body.dataset.vscodeThemeKind = 'vscode-dark'",
            "document.body.dataset.vscodeThemeKind = 'vscode-light'",
        ),
        # Jupyter Lab's ThemeManager sets this data-attribute on <body>
        # (moved there from a child node in jupyterlab/jupyterlab#6554
        # precisely so that page-level code can read it), and updates it
        # live whenever the user switches theme from the settings menu.
        (
            "jupyterlab",
            'data-jp-theme-light="true"',
            "document.body.dataset.jpThemeLight = 'false'",
            "document.body.dataset.jpThemeLight = 'true'",
        ),
    ],
)
def test_dark_class_follows_theme_change_after_render(
    tmp_path, host, initial_attrs, switch_to_dark_js, switch_to_light_js
):
    html_path = tmp_path / "table.html"
    html_path.write_text(
        render_offline_notebook_html(initial_attrs),
        encoding="utf-8",
    )

    with sync_playwright() as p:
        browser = p.chromium.launch()
        try:
            page = browser.new_page(viewport={"width": 500, "height": 400})
            errors = []
            page.on("pageerror", lambda exc: errors.append(str(exc)))
            page.goto(html_path.as_uri())
            page.wait_for_selector("table.dataTable")

            assert errors == []
            assert "dark" not in page.evaluate("document.documentElement.className")

            # The user switches to a dark theme, and the host updates the
            # data-attribute on <body> in place, without reloading the page.
            page.evaluate(switch_to_dark_js)
            page.wait_for_function(
                "document.documentElement.className.includes('dark')"
            )

            assert errors == []
            assert "dark" in page.evaluate("document.documentElement.className")

            # And back to light.
            page.evaluate(switch_to_light_js)
            page.wait_for_function(
                "!document.documentElement.className.includes('dark')"
            )

            assert errors == []
            assert "dark" not in page.evaluate("document.documentElement.className")
        finally:
            browser.close()
