"""Browser-based regression test for https://github.com/mwouts/itables/issues/426

itables' regular table cells are transparent by design, so that they blend
into the host page's own background instead of hard-coding a color (see the
dark-mode fixed-columns fix, issue #564's test). That works for the plain
HTML/notebook-cell output, which sits directly in a themed output area, but
the container into which ipywidgets (e.g. VS Code's Jupyter extension, or
any other `@jupyter-widgets/html-manager`-based host) mounts a widget's view
has its own opaque, always-white background -- so the transparent table
cells used to show through to white instead of the notebook's dark theme,
even though the dark-mode detection itself (the `dark` class, and controls
like the search box) worked correctly.

VS Code specifically goes one step further: it wraps *every* ipywidget
output in one or more `.cell-output-ipywidget-background` containers,
hardcoded to white regardless of the editor's theme, which showed up as a
thick white border around the widget even after `.itables_anywidget` itself
was correctly painted dark.

It requires Playwright and its Chromium browser, which are not part of the
default test dependencies. Run it locally with the dedicated `playwright`
pixi environment, see docs/developing.md.
"""

import functools
import http.server
import json
import shutil
import threading

import pytest

pytest.importorskip("playwright")

try:
    import pandas as pd  # noqa: F401
except ImportError:
    pytest.skip("Pandas is not available", allow_module_level=True)

try:
    import anywidget  # noqa: F401
except ImportError:
    pytest.skip("anywidget is not available", allow_module_level=True)

from playwright.sync_api import (  # noqa: E402  # pyright: ignore[reportMissingImports]
    sync_playwright,
)

from itables.sample_dfs import get_dict_of_test_dfs  # noqa: E402
from itables.utils import find_package_file  # noqa: E402
from itables.widget import ITable  # noqa: E402


def render_widget_page(tmp_path, body_dataset_attrs: str) -> http.server.HTTPServer:
    """Serve a page that renders the `ITable` anywidget the same way a real
    widget front-end does: import the built `widget.js`/`widget.css`, and
    call `render({model, el})` with a stub model exposing the widget's
    traits. HTTP (not file://) is required because the widget bundle is
    loaded as an ES module, and Chromium blocks module imports over
    file://."""
    df = get_dict_of_test_dfs()["int_float_str"]
    table = ITable(df, selected_rows=[0, 2, 5], select=True)
    payload = json.dumps(
        {
            "dt_args": table._dt_args,
            "caption": table.caption,
            "classes": table.classes,
            "style": table._style,
            "selected_rows": table.selected_rows,
        }
    )

    static_dir = find_package_file("widget/static")
    shutil.copy(static_dir / "widget.js", tmp_path / "widget.js")
    shutil.copy(static_dir / "widget.css", tmp_path / "widget.css")

    html = f"""<html>
<head>
<link rel="stylesheet" href="widget.css">
<style>
/* Mimics VS Code's own CSS: hardcoded white, regardless of theme. */
.cell-output-ipywidget-background {{ background-color: white; }}
</style>
</head>
<body {body_dataset_attrs}>
<script id="payload" type="application/json">{payload}</script>
<script type="module">
import widgetModule from './widget.js';
const {{ render }} = widgetModule;

const payload = JSON.parse(document.getElementById('payload').textContent);
const data = {{
    _dt_args: payload.dt_args,
    caption: payload.caption,
    classes: payload.classes,
    _style: payload.style,
    selected_rows: payload.selected_rows,
}};
const model = {{
    get(key) {{ return data[key]; }},
    set(key, val) {{ data[key] = val; }},
    on() {{}},
    save_changes() {{}},
}};
const outer = document.createElement('div');
outer.className = 'output cell-output-ipywidget-background';
const inner = document.createElement('div');
inner.className = 'cell-output-ipywidget-background';
outer.appendChild(inner);
document.body.appendChild(outer);

const el = document.createElement('div');
inner.appendChild(el);
render({{ model, el }});
</script>
</body>
</html>
"""
    (tmp_path / "index.html").write_text(html, encoding="utf-8")

    handler = functools.partial(
        http.server.SimpleHTTPRequestHandler, directory=str(tmp_path)
    )
    httpd = http.server.HTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd


@pytest.mark.parametrize(
    "body_dataset_attrs, expect_dark",
    [
        ('data-vscode-theme-kind="vscode-dark"', True),
        ('data-vscode-theme-kind="vscode-light"', False),
    ],
)
def test_widget_container_background_matches_dark_mode(
    tmp_path, body_dataset_attrs, expect_dark
):
    httpd = render_widget_page(tmp_path, body_dataset_attrs)
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            try:
                page = browser.new_page(viewport={"width": 500, "height": 400})
                errors = []
                page.on("pageerror", lambda exc: errors.append(str(exc)))
                page.goto(f"http://127.0.0.1:{httpd.server_address[1]}/index.html")
                page.wait_for_selector("table.dataTable")

                assert errors == []
                assert expect_dark == (
                    "dark" in page.evaluate("document.documentElement.className")
                )

                container_background = page.evaluate(
                    """
                    () => getComputedStyle(
                      document.querySelector('.itables_anywidget')
                    ).backgroundColor
                    """
                )
                # The widget's own container must carry an explicit
                # background matching the detected theme: itables' table
                # cells are transparent by design and rely on this to show
                # through, instead of the host's default (white) background.
                expected = "rgb(33, 37, 41)" if expect_dark else "rgb(255, 255, 255)"
                assert container_background == expected

                # VS Code's own (hardcoded-white) wrapper(s) around the
                # widget must also be repainted, or a white border remains
                # around an otherwise correctly-dark table.
                wrapper_backgrounds = page.evaluate(
                    """
                    () => Array.from(
                      document.querySelectorAll('.cell-output-ipywidget-background')
                    ).map(el => getComputedStyle(el).backgroundColor)
                    """
                )
                assert wrapper_backgrounds == [expected, expected]
            finally:
                browser.close()
    finally:
        httpd.shutdown()
