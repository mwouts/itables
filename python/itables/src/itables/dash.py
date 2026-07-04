"""The itables.dash module now lives in pydatatables.dash"""

from pydatatables.dash import (  # noqa: F401
    ITABLE_PROPERTIES,
    DataTable,
    PyDataTablesRendererOutputs,
    updated_itable_outputs,
)

from .version import __version__

# The historical names of the itables.dash objects
ITable = DataTable
ITableOutputs = PyDataTablesRendererOutputs

__all__ = [
    "ITable",
    "ITABLE_PROPERTIES",
    "ITableOutputs",
    "updated_itable_outputs",
    "__version__",
]
