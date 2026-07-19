"""Prepare docs/ for the JupyterLite build that jupyterlite-sphinx triggers.

Run this before `jupyter-book build docs`. It does two things:

1. Stages a copy of the doc pages under docs/_contents/docs/.

   jupyterlite-sphinx always includes docs/_contents as one of the directories
   it feeds to `jupyter lite build --contents`, and it merges each of those
   directories' *children* into the JupyterLite content root (so `--contents
   docs/apps` would land as `files/*.md`, not `files/apps/*.md`).

   The "rocket icon" launch button added by sphinx-book-theme, on the other
   hand, links to `<jupyterlite_url>?path=<path_to_docs>/<page>.md` -- i.e. it
   expects our `path_to_docs` (`docs`, see docs/_config.yml) to be part of the
   JupyterLite content tree. So we stage the doc pages one level deeper, under
   docs/_contents/docs/, to reproduce that expected prefix.

2. Generates docs/jupyter-lite.json, so the Pyodide kernel preloads the latest
   published itables wheel from PyPI at startup. Without this, `import
   itables` would need an explicit `%pip install itables` cell -- there is no
   auto-install-on-import for packages that aren't part of the base Pyodide
   distribution.
"""

import json
import shutil
import urllib.request
from pathlib import Path

DOCS_DIR = Path(__file__).parent


def stage_doc_pages() -> None:
    staged_docs = DOCS_DIR / "_contents" / "docs"
    if staged_docs.exists():
        shutil.rmtree(staged_docs)
    staged_docs.mkdir(parents=True)

    for name in ["quick_start.md", "apps", "options", "fallbacks"]:
        src = DOCS_DIR / name
        dst = staged_docs / name
        if src.is_dir():
            shutil.copytree(src, dst)
        else:
            shutil.copy2(src, dst)


def latest_itables_wheel_url() -> str:
    with urllib.request.urlopen("https://pypi.org/pypi/itables/json") as response:
        metadata = json.load(response)
    for file_info in metadata["urls"]:
        if file_info["packagetype"] == "bdist_wheel":
            return file_info["url"]
    raise RuntimeError("No wheel found for the latest itables release on PyPI")


def write_jupyter_lite_config() -> None:
    config = {
        "jupyter-config-data": {
            "litePluginSettings": {
                "@jupyterlite/pyodide-kernel-extension:kernel": {
                    "loadPyodideOptions": {
                        "packages": [latest_itables_wheel_url()],
                    },
                },
            },
        },
    }
    (DOCS_DIR / "jupyter-lite.json").write_text(json.dumps(config, indent=2) + "\n")


if __name__ == "__main__":
    stage_doc_pages()
    write_jupyter_lite_config()
