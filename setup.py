import re
import subprocess
from io import open
from pathlib import Path

from setuptools import find_packages, setup

this_directory = Path(__file__).parent
with open(str(this_directory / "README.md"), encoding="utf-8") as f:
    long_description = f.read()

with open(str(this_directory / "itables/version.py")) as f:
    version_file = f.read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    version = version_match.group(1)

subprocess.check_call(["npm", "install", "--prefix", "itables/dt_package"])
subprocess.check_call(["npm", "run", "build", "--prefix", "itables/dt_package"])

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
            "dt_bundle/dt.css",
            "dt_bundle/dt.js",
        ]
    },
    tests_require=["pytest", "pytz"],
    install_requires=["IPython", "pandas", "numpy"],
    extras_require={"polars": ["polars", "pyarrow"]},
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
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
