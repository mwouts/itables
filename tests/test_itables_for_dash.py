import os
import sys

import pytest

from itables.dash import ITable, itables_for_dash_is_available

if not itables_for_dash_is_available:
    pytestmark = pytest.mark.skip(reason="itables_for_dash is not available")


def check_ressource(relative_package_path, namespace, **kwargs):
    ressource_file = sys.modules[namespace].__file__
    assert isinstance(ressource_file, str), ressource_file
    module_path = os.path.join(os.path.dirname(ressource_file), relative_package_path)
    assert os.path.exists(module_path), module_path


def test_itable_component_ressources():
    for js in ITable._js_dist:  # type: ignore
        check_ressource(**js)
    for css in ITable._css_dist:  # type: ignore
        check_ressource(**css)


def test_create_empty_table():
    ITable(id="test")
