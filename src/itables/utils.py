from io import open
from pathlib import Path

UNPKG_DT_BUNDLE_URL = "https://www.unpkg.com/dt_for_itables@2.0.7/dt_bundle.js"
UNPKG_DT_BUNDLE_CSS = UNPKG_DT_BUNDLE_URL.replace(".js", ".css")


def find_package_file(*path):
    """Return the full path to a file from the itables package"""
    current_path = Path(__file__).parent
    return Path(current_path, *path)


def read_package_file(*path):
    """Return the content of a file from the itables package"""
    with open(find_package_file(*path), encoding="utf-8") as fp:
        return fp.read()
