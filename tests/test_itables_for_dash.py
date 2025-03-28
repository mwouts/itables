import os
import sys

import pytest

from itables.dash import ITable, ITableComponent, itables_for_dash_is_available

if not itables_for_dash_is_available:
    pytestmark = pytest.mark.skip(reason="itables_for_dash is not available")


def check_ressource(relative_package_path, namespace, **kwargs):
    module_path = os.path.join(
        os.path.dirname(sys.modules[namespace].__file__), relative_package_path
    )
    assert os.path.exists(module_path), module_path


def test_itable_component_ressources():
    for js in ITableComponent._js_dist:
        check_ressource(**js)
    for css in ITableComponent._css_dist:
        check_ressource(**css)


def test_create_empty_table():
    ITable(id="test")
