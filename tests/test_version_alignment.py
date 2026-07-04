"""The four ITables packages are released together with the same version number,
and the cross dependencies are pinned to that exact version."""

import re
from pathlib import Path

PYTHON_PACKAGES = Path(__file__).parent.parent / "python"


def get_version(package: str) -> str:
    version_file = next((PYTHON_PACKAGES / package / "src").glob("*/version.py"))
    match = re.search(r'__version__ = "(.*)"', version_file.read_text())
    assert match is not None, version_file
    return match.group(1)


def get_dependencies(package: str) -> str:
    pyproject = (PYTHON_PACKAGES / package / "pyproject.toml").read_text()
    match = re.search(r"^dependencies = (\[.*\])$", pyproject, flags=re.MULTILINE)
    assert match is not None, package
    return match.group(1)


def test_all_versions_are_aligned():
    versions = {
        package: get_version(package)
        for package in ["itables_core", "pydatatables", "pyaggrid", "itables"]
    }
    assert len(set(versions.values())) == 1, versions


def test_cross_dependencies_are_pinned_to_the_common_version():
    version = get_version("itables_core")
    assert get_dependencies("pydatatables") == f'["itables_core=={version}"]'
    assert get_dependencies("pyaggrid") == f'["itables_core=={version}"]'
    assert (
        get_dependencies("itables")
        == f'["pydatatables=={version}", "pyaggrid=={version}"]'
    )
