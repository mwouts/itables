"""The itables widget now lives in pydatatables.widget"""

from pydatatables.widget import DataTable, __version__  # noqa: F401

# The historical name of the itables widget
ITable = DataTable

__all__ = ["ITable", "DataTable", "__version__"]
