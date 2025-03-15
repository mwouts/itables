from .ITable import ITable as ITableComponent
from .properties import (
    ITABLE_PROPERTIES,
    ITableOutputs,
    get_itable_component_kwargs,
    updated_itable_outputs,
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


ITableComponent._js_dist = _js_dist
ITableComponent._css_dis = _css_dist


def ITable(*, id, **kwargs):
    """Return an ITable component with the given id"""
    return ITableComponent(id=id, **get_itable_component_kwargs(**kwargs))


__all__ = [
    "ITable",
    "ITableComponent",
    "ITABLE_PROPERTIES",
    "get_itable_component_kwargs",
    "ITableOutputs",
    "updated_itable_outputs",
    "__version__",
]
