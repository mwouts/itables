import re
from pathlib import Path

import pytest


def replace_issue_number_with_links(text):
    return re.sub(
        r"([^\[])#([0-9]+)",
        r"\1[#\2](https://github.com/mwouts/itables/issues/\2)",
        text,
    )


@pytest.mark.parametrize(
    "input,output",
    [
        (
            "Issue #535",
            "Issue [#535](https://github.com/mwouts/itables/issues/535)",
        ),
        (
            "Multiline\ntext (#123)",
            "Multiline\ntext ([#123](https://github.com/mwouts/itables/issues/123))",
        ),
    ],
)
def test_replace_issue_numbers_with_links(input, output):
    assert replace_issue_number_with_links(input) == output


def test_update_changelog():
    changelog_file = Path(__file__).parent.parent / "docs" / "changelog.md"
    cur_text = changelog_file.read_text()
    new_text = replace_issue_number_with_links(cur_text)
    if cur_text != new_text:
        changelog_file.write_text(new_text)  # pragma: no cover
