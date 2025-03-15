from .ITable import ITable
from .properties import (
    ITABLE_PROPERTIES,
    get_itable_properties,
    get_itable_properties_as_list,
)

_js_dist = [
    {"namespace": "itables_for_dash", "relative_package_path": name, **kwargs}
    for name, kwargs in {
        "async-ITable.js": {"async": True},
        "async-ITable.js.map": {"dynamic": True},
        "itables_for_dash.min.js": {},
        "itables_for_dash.min.js.map": {"dynamic": True},
    }.items()
]

_css_dist = []


ITable._js_dist = _js_dist
ITable._css_dis = _css_dist

__all__ = [
    "ITable",
    "ITABLE_PROPERTIES",
    "get_itable_properties",
    "get_itable_properties_as_list",
    "__version__",
]
