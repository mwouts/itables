# Test setup.py with and without the import requests


import subprocess
import sys
from unittest import mock

import pytest


def test_setup_with_requests():
    with pytest.raises(subprocess.CalledProcessError) as excinfo:
        subprocess.check_call([sys.executable, "setup.py", "install"], cwd="tests")
        assert excinfo.value.returncode == 0


def test_setup_without_requests():
    with mock.patch.dict(sys.modules, {"requests": None}):
        with pytest.raises(subprocess.CalledProcessError) as excinfo:
            subprocess.check_call([sys.executable, "setup.py", "install"], cwd="tests")
            assert excinfo.value.returncode == 2
