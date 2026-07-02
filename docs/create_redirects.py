"""Create HTML redirect stubs for the URLs of the previous documentation.

Jupyter Book v1 served every page at '<path>.html', while MyST (Jupyter Book
v2) serves it at '<path>' with underscores replaced with hyphens. This script
writes a redirect stub at each former page URL. It also restores the
redirects that were previously implemented with sphinxext-rediraffe (see
docs/_config.yml prior to the transition to Jupyter Book v2).

Usage: python docs/create_redirects.py docs/_build/html
"""

import os.path
import sys
from pathlib import Path

import yaml

# The redirects formerly implemented with sphinxext-rediraffe,
# mapping the old page name to the current page
REDIRECTS = {
    "advanced_parameters": "options/options",
    "extensions": "options/buttons",
    "select": "options/select",
    "custom_css": "css",
    "dash": "apps/dash",
    "html_export": "apps/html",
    "shiny": "apps/shiny",
    "quarto": "apps/quarto",
    "streamlit": "apps/streamlit",
    "widget": "apps/widget",
    "sample_dataframes": "pandas_dataframes",
}

TEMPLATE = """<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <meta http-equiv="refresh" content="0; url={url}">
    <link rel="canonical" href="{url}">
    <title>Redirecting&hellip;</title>
  </head>
  <body>
    <p>This page has moved to <a href="{url}">{url}</a>.</p>
  </body>
</html>
"""


def iter_toc_files(entries):
    for entry in entries:
        if "file" in entry:
            yield entry["file"]
        yield from iter_toc_files(entry.get("children", []))


def slug(page):
    """The URL at which MyST serves the given page"""
    return page.replace("_", "-")


def relative_url(target, origin_html_file):
    """The URL of the target page, relative to the given redirect stub"""
    url = os.path.relpath(target, os.path.dirname(origin_html_file))
    return "./" if url == "." else url


def create_redirects(html_dir):
    docs_dir = Path(__file__).parent
    config = yaml.safe_load((docs_dir / "myst.yml").read_text())
    pages = [file.removesuffix(".md") for file in iter_toc_files(config["project"]["toc"])]

    # The first page in the TOC is served at the site root
    targets = {pages[0]: "."}
    targets.update({page: slug(page) for page in pages[1:]})
    targets.update({old: slug(target) for old, target in REDIRECTS.items()})

    for page, target in targets.items():
        stub = html_dir / f"{page}.html"
        if stub.exists():
            # Don't overwrite pages exported by the build itself
            continue
        stub.parent.mkdir(parents=True, exist_ok=True)
        stub.write_text(TEMPLATE.format(url=relative_url(target, f"{page}.html")))
        print(f"{page}.html -> {target}")


if __name__ == "__main__":
    create_redirects(Path(sys.argv[1]))
