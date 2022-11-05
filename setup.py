import re
from os import path
from pathlib import Path

import requests
from setuptools import find_packages, setup

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

with open(path.join(this_directory, "itables/version.py")) as f:
    version_file = f.read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    version = version_match.group(1)

external = Path(__file__).parent / "itables" / "external"
external.mkdir(exist_ok=True)
for name, url in [
    ("jquery.min.js", "https://code.jquery.com/jquery-3.6.0.min.js"),
    (
        "jquery.dataTables.min.css",
        "https://cdn.datatables.net/1.12.1/css/jquery.dataTables.min.css",
    ),
    (
        "jquery.dataTables.mjs",
        "https://cdn.datatables.net/1.12.1/js/jquery.dataTables.mjs",
    ),
]:
    r = requests.get(url)
    (external / name).write_bytes(r.content)

setup(
    name="itables",
    version=version,
    author="Marc Wouts",
    author_email="marc.wouts@gmail.com",
    description="Interactive Tables in Jupyter",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mwouts/itables",
    packages=find_packages(exclude=["tests"]),
    package_data={
        "itables": [
            "html/*",
            "html/column_filters/*",
            "samples/*.csv",
            "external/*",
        ]
    },
    tests_require=["pytest"],
    install_requires=["IPython", "pandas"],
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Framework :: Jupyter",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
