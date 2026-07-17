"""Generate and execute short demo notebooks, and save them under
tests/data/ so that the static-preview fallback (see #575) can be
visually inspected by viewing these files on GitHub: since GitHub's own
notebook preview page does not execute the <script> tags in our HTML
output (they're inserted into the page's DOM instead of being parsed as
part of it, so they stay inert), the static-preview table - shown by
default, ahead of the initially-hidden interactive table - is what shows
up there, while a real (trusted, JavaScript-capable) Jupyter session
swaps the two around and shows the interactive table instead.

Like test_to_html_datatable.py, the reference notebook is created (and
the test fails, asking you to review it) the first time it's missing,
and compared byte-for-byte on every following run.
"""

import copy
import json
import re
from pathlib import Path

import pytest

nbformat = pytest.importorskip("nbformat")
pytest.importorskip("nbconvert")
pytest.importorskip("ipykernel")
pytest.importorskip("pandas")
pytest.importorskip("jinja2")  # required for pandas.DataFrame.style

from nbconvert.preprocessors import ExecutePreprocessor  # noqa: E402
from nbformat.v4 import (  # noqa: E402
    new_code_cell,
    new_markdown_cell,
    new_notebook,
)

from itables.version import __version__ as itables_version  # noqa: E402

NOTEBOOK_DIR = Path(__file__).parent / "data" / "static_preview_notebooks"

with open(Path(__file__).parent / "../packages/dt_for_itables/package.json") as fp:
    DT_FOR_ITABLES_VERSION = json.load(fp)["version"]


@pytest.fixture(scope="module")
def notebook_kernel_name():
    from ipykernel.kernelspec import install
    from jupyter_client.kernelspec import KernelSpecManager

    name = "itables-test-static-preview"
    install(user=True, kernel_name=name, display_name=name)
    yield name
    KernelSpecManager().remove_kernel_spec(name)


def _build_notebook():
    nb = new_notebook()
    nb.cells = [
        new_markdown_cell(
            "This notebook demonstrates the static preview fallback for "
            "itables (see [issue #575]"
            "(https://github.com/mwouts/itables/issues/575)). The tables "
            "below are interactive when JavaScript can run - e.g. when "
            "you execute this notebook yourself in a trusted Jupyter "
            "session. If JavaScript can't run - e.g. GitHub's static "
            "preview of this file - a plain HTML table is shown instead."
        ),
        new_code_cell(
            "import pandas as pd\n"
            "import itables\n"
            "\n"
            "itables.init_notebook_mode(connected=True)\n"
            "\n"
            "df = pd.DataFrame(\n"
            "    {\n"
            '        "country": ["France", "Germany", "Italy", "Spain"],\n'
            '        "capital": ["Paris", "Berlin", "Rome", "Madrid"],\n'
            '        "population_millions": [68.0, 84.5, 59.0, 47.4],\n'
            "    }\n"
            ').set_index("country")'
        ),
        new_markdown_cell("## The bare `df` repr"),
        new_code_cell("df"),
        new_markdown_cell("## `itables.show(df)`"),
        new_code_cell("itables.show(df)"),
        new_markdown_cell(
            "## A table with a caption\n"
            "\n"
            "The caption is shown below the table, like in the interactive "
            "table. In the static preview it is rendered as a `<tfoot>` row "
            "rather than a `<caption>` element, because GitHub's notebook "
            "viewer strips `<caption>` tags from the output (the leftover text "
            "would then be pushed above the table)."
        ),
        new_code_cell(
            'itables.show(df, caption="Population of some European countries")'
        ),
        new_markdown_cell(
            "## A table with a caption above it\n"
            "\n"
            "With `caption-side:top` in the `style` option, the caption is "
            "placed above the table instead - here in a leading `<thead>` row."
        ),
        new_code_cell(
            "itables.show(\n"
            "    df,\n"
            '    caption="Population of some European countries",\n'
            '    style="table-layout:auto;width:auto;margin:auto;caption-side:top",\n'
            ")"
        ),
        new_markdown_cell(
            "## A Pandas Styler\n"
            "\n"
            "Styler objects are already a static HTML rendering, so their "
            "static preview reuses that same HTML directly - see "
            "[`test_static_preview_fallback_shows_styler_table_html`]"
            "(https://github.com/mwouts/itables/blob/main/tests/test_pandas_style.py)."
        ),
        new_code_cell(
            "itables.show(\n"
            '    df.style.highlight_max(color="lightgreen"), allow_html=True\n'
            ")"
        ),
    ]
    return nb


def _stable_text(nb) -> str:
    """Strip the parts of an executed notebook that are not reproducible
    across runs/environments (timestamps, cell ids, Python patch version),
    and return its serialized text. The itables/dt_for_itables version
    numbers are left as-is, so that the saved notebook remains a genuine,
    presentable example when viewed on GitHub."""
    nb = copy.deepcopy(nb)
    nb["metadata"].pop("language_info", None)
    for i, cell in enumerate(nb["cells"]):
        # A missing id gets replaced by a random one on write/validation,
        # so we set a deterministic one instead of just removing it
        cell["id"] = f"cell-{i}"
        cell.get("metadata", {}).pop("execution", None)
    return nbformat.writes(nb)


_TABLE_ID_RE = re.compile(
    r"itables_[0-9a-f]{8}_[0-9a-f]{4}_[0-9a-f]{4}_[0-9a-f]{4}_[0-9a-f]{12}"
)
# Pandas Styler objects generate their own random id (T_xxxxx) for CSS scoping,
# cf. check_table_id()'s "T_" + str(uuid.uuid4())[:5] fallback for Styler objects
_STYLER_ID_RE = re.compile(r"T_[0-9a-f]{5}")


def _version_independent(text: str) -> str:
    """Replace the itables/dt_for_itables version numbers, and the randomly
    generated table_id (a new uuid4 on every execution, since the notebook
    cells don't pass an explicit table_id), with placeholders - mirroring
    test_to_html_datatable.py's approach - so that comparisons don't require
    regenerating the reference notebook on every version bump or run."""
    text = text.replace(itables_version, "{itables_version}")
    text = text.replace(DT_FOR_ITABLES_VERSION, "{dt_for_itables_version}")
    text = _TABLE_ID_RE.sub("itables_{table_id}", text)
    text = _STYLER_ID_RE.sub("T_{table_id}", text)
    return text


def _html_outputs(cell):
    return [
        output["data"]["text/html"]
        for output in cell.get("outputs", [])
        if "data" in output and "text/html" in output["data"]
    ]


def test_static_preview_notebook(notebook_kernel_name):
    nb = _build_notebook()
    ExecutePreprocessor(kernel_name=notebook_kernel_name, timeout=60).preprocess(nb)

    df_repr_cell, show_cell, caption_cell, caption_top_cell, styler_cell = (
        nb.cells[3],
        nb.cells[5],
        nb.cells[7],
        nb.cells[9],
        nb.cells[11],
    )
    for cell in (df_repr_cell, show_cell, caption_cell, caption_top_cell, styler_cell):
        assert not any(
            output.get("output_type") == "error" for output in cell.get("outputs", [])
        ), cell["outputs"]
        html_outputs = _html_outputs(cell)
        assert html_outputs, f"No text/html output found in cell: {cell['source']}"
        html = "".join(html_outputs[0])
        assert "_fallback" in html
        assert "France" in html

    def _fallback_of(cell):
        return "".join(_html_outputs(cell)[0]).split('<div id="', 1)[1].split(">", 1)[1]

    # the caption is rendered as a table row, not a <caption> tag (which
    # GitHub strips), so it survives on GitHub (cf. #575): below the table
    # (a <tfoot> row) by default, ...
    caption_fallback = _fallback_of(caption_cell)
    assert "<caption" not in caption_fallback
    tfoot = caption_fallback.split("<tfoot>", 1)[1].split("</tfoot>", 1)[0]
    assert "Population of some European countries" in tfoot

    # ... or above it (a leading <thead> row) with caption-side:top
    caption_top_fallback = _fallback_of(caption_top_cell)
    assert "<caption" not in caption_top_fallback
    thead = caption_top_fallback.split("<thead>", 1)[1].split("</thead>", 1)[0]
    assert "Population of some European countries" in thead
    assert thead.index("Population of some European countries") < thead.index("<th")

    styler_fallback = (
        "".join(_html_outputs(styler_cell)[0]).split('<div id="', 1)[1].split(">", 1)[1]
    )
    assert "no static preview" not in styler_fallback

    generated = _stable_text(nb)

    ref_file = NOTEBOOK_DIR / "static_preview_demo.ipynb"
    if not ref_file.exists():
        ref_file.parent.mkdir(parents=True, exist_ok=True)
        ref_file.write_text(generated)
        assert (
            False
        ), f"Reference notebook created at {ref_file}. Please verify it and run the test again."

    # ref_file may have a trailing newline added by the end-of-file-fixer
    # pre-commit hook, which nbformat.writes() doesn't necessarily add.
    expected = ref_file.read_text()
    assert _version_independent(generated.rstrip("\n")) == _version_independent(
        expected.rstrip("\n")
    ), "Generated notebook does not match reference."
