from io import open
from pathlib import Path

UNPKG_DT_BUNDLE_URL = "https://www.unpkg.com/pydatatables-assets@3.0.0/dt_bundle.js"
UNPKG_DT_BUNDLE_CSS = UNPKG_DT_BUNDLE_URL.replace(".js", ".css")
UNPKG_DT_BUNDLE_URL_NO_VERSION = (
    "https://www.unpkg.com/pydatatables-assets/dt_bundle.js"
)
UNPKG_DT_BUNDLE_CSS_NO_VERSION = (
    "https://www.unpkg.com/pydatatables-assets/dt_bundle.css"
)


def find_package_file(*path: str) -> Path:
    """Return the full path to a file from the itables package"""
    current_path = Path(__file__).parent
    return Path(current_path, *path)


def read_package_file(*path: str) -> str:
    """Return the content of a file from the itables package"""
    with open(find_package_file(*path), encoding="utf-8") as fp:
        return fp.read()
