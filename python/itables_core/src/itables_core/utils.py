from io import open
from pathlib import Path


def find_package_file(*path: str) -> Path:
    """Return the full path to a file from the itables_core package"""
    current_path = Path(__file__).parent
    return Path(current_path, *path)


def read_package_file(*path: str) -> str:
    """Return the content of a file from the itables_core package"""
    with open(find_package_file(*path), encoding="utf-8") as fp:
        return fp.read()


def replace_value(
    template: str, pattern: str, value: str, expected_count: int = 1
) -> str:
    """Set the given pattern to the desired value in the template,
    after making sure that the pattern is found exactly once."""
    count = template.count(pattern)
    if count != expected_count:
        raise ValueError(
            f"{pattern=} was found {count} times in template, expected {expected_count}."
        )
    return template.replace(pattern, value)
