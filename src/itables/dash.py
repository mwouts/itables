from itables import __version__
from itables_for_dash.properties import (
    ITABLE_PROPERTIES,
    ITableOutputs,
    get_itable_component_kwargs,
    updated_itable_outputs,
)

try:
    from itables_for_dash import ITable, ITableComponent  # type: ignore
except ImportError as e:
    import_error = e

    class ITableComponent:
        def __init__(self, **kwargs):
            raise import_error

    class ITable(ITableComponent):
        pass

    itables_for_dash_is_available = False
else:
    itables_for_dash_is_available = True

__all__ = [
    "ITable",
    "ITableComponent",
    "ITABLE_PROPERTIES",
    "get_itable_component_kwargs",
    "ITableOutputs",
    "updated_itable_outputs",
    "__version__",
]
