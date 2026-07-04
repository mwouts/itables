"""The itables.shiny module now lives in pydatatables.shiny"""

from pydatatables.shiny import DataTable, init_pydatatables  # noqa: F401

# The historical names of the itables.shiny functions
DT = DataTable
init_itables = init_pydatatables
