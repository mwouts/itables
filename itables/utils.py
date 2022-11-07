import os
from io import open


def find_package_file(*path):
    """Return the full path to a file from the itables package"""
    current_path = os.path.dirname(__file__)
    return os.path.join(current_path, *path)


def read_package_file(*path):
    """Return the content of a file from the itables package"""
    with open(find_package_file(*path), encoding="utf-8") as fp:
        return fp.read()
