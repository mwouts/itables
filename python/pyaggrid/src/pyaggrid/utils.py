from io import open
from pathlib import Path

AG_GRID_ESM_URL = "https://cdn.jsdelivr.net/npm/ag-grid-community@35.3.1/+esm"


def find_package_file(*path: str) -> Path:
    """Return the full path to a file from the pyaggrid package"""
    current_path = Path(__file__).parent
    return Path(current_path, *path)


def read_package_file(*path: str) -> str:
    """Return the content of a file from the pyaggrid package"""
    with open(find_package_file(*path), encoding="utf-8") as fp:
        return fp.read()
