from io import open
from pathlib import Path

UNPKG_PYAGGRID_BUNDLE_URL = "https://www.unpkg.com/pyaggrid/aggrid_bundle.js"
UNPKG_PYAGGRID_BUNDLE_URL_NO_VERSION = "https://www.unpkg.com/pyaggrid/aggrid_bundle.js"


def find_package_file(*path: str) -> Path:
    """Return the full path to a file from the pyaggrid package"""
    current_path = Path(__file__).parent
    return Path(current_path, *path)


def read_package_file(*path: str) -> str:
    """Return the content of a file from the pyaggrid package"""
    with open(find_package_file(*path), encoding="utf-8") as fp:
        return fp.read()
