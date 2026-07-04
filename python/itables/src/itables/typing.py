"""The itables.typing module now lives in pydatatables.typing"""

from pydatatables.typing import *  # noqa: F401,F403
from pydatatables.typing import (  # noqa: F401
    DataTableOptions,
    PyDataTablesOptions,
    PyDataTablesRendererOptions,
)

# The historical names of the itables typed dicts
ITableOptions = PyDataTablesOptions
DTForITablesOptions = PyDataTablesRendererOptions
