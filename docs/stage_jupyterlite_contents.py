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

2. Generates docs/jupyter-lite.json, so the Pyodide kernel preloads, at
   startup, the packages the staged doc pages actually import: the latest
   published itables wheel from PyPI, and pandas (a package built into the
   Pyodide distribution -- unlike itables, it has compiled extensions, so it
   must come from Pyodide's own WASM build rather than PyPI). Without this,
   `import itables` / `import pandas` would need an explicit `%pip install`
   cell -- there is no auto-install-on-import for packages that aren't part
   of the base Pyodide distribution.

Each staged .md file also gets a `language_info` key added to its YAML
frontmatter (only in the staged _copy_ -- the real docs/*.md are untouched).
Without it, JupyterLite shows a "select kernel" dialog instead of picking the
Pyodide kernel automatically: our frontmatter's `kernelspec.name` is
`python3` (needed for the local kernel that builds the static docs), but
JupyterLite's Pyodide kernel is named `python`. JupyterLab's fallback for a
mismatched kernel name only kicks in when it can find a *single* installed
kernel matching `language_info.name` -- and that field is normally filled in
by the kernel itself after running the notebook once, which never happens
for a freshly-authored .md file.
"""

import json
import shutil
import urllib.request
from pathlib import Path

import yaml

DOCS_DIR = Path(__file__).parent
FRONTMATTER_DELIMITER = "---\n"


def add_language_info(markdown: str) -> str:
    if not markdown.startswith(FRONTMATTER_DELIMITER):
        return markdown
    end = markdown.find(f"\n{FRONTMATTER_DELIMITER}", len(FRONTMATTER_DELIMITER))
    if end == -1:
        return markdown

    frontmatter = yaml.safe_load(markdown[len(FRONTMATTER_DELIMITER) : end])
    kernelspec = frontmatter.get("kernelspec")
    if not kernelspec or "language_info" in frontmatter:
        return markdown

    frontmatter["language_info"] = {"name": kernelspec["language"]}
    body = markdown[end + len(f"\n{FRONTMATTER_DELIMITER}") :]
    return (
        FRONTMATTER_DELIMITER
        + yaml.safe_dump(frontmatter, sort_keys=False)
        + FRONTMATTER_DELIMITER
        + body
    )


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

    for md_file in staged_docs.rglob("*.md"):
        md_file.write_text(add_language_info(md_file.read_text()))


def latest_itables_wheel_url() -> str:
    with urllib.request.urlopen("https://pypi.org/pypi/itables/json") as response:
        metadata = json.load(response)
    for file_info in metadata["urls"]:
        if file_info["packagetype"] == "bdist_wheel":
            return file_info["url"]
    raise RuntimeError("No wheel found for the latest itables release on PyPI")


def write_jupyter_lite_config() -> None:
    # "pandas" is loaded by name, from Pyodide's own distribution; itables is
    # pure Python, so a regular PyPI wheel works fine.
    packages = ["pandas", latest_itables_wheel_url()]
    config = {
        "jupyter-config-data": {
            "litePluginSettings": {
                "@jupyterlite/pyodide-kernel-extension:kernel": {
                    "loadPyodideOptions": {
                        "packages": packages,
                    },
                },
            },
        },
    }
    (DOCS_DIR / "jupyter-lite.json").write_text(json.dumps(config, indent=2) + "\n")


if __name__ == "__main__":
    stage_doc_pages()
    write_jupyter_lite_config()
