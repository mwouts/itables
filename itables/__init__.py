from .javascript import show, load_datatables
from .version import __version__

load_datatables(
    required_modules={
        "datatables.net": 'https://cdn.datatables.net/1.10.22/js/jquery.dataTables.min',
        "datatables.net-buttons": "https://cdn.datatables.net/buttons/1.6.5/js/dataTables.buttons.min",
        "datatables.net-html5": "https://cdn.datatables.net/buttons/1.6.5/js/buttons.html5.min"},
    required_css=[
        '<link rel="stylesheet" type="text/css" href = "https://cdn.datatables.net/1.10.22/css/jquery.dataTables.min.css" > ',
        '<link rel="stylesheet" type="text/css" href = "https://cdn.datatables.net/buttons/1.6.5/css/buttons.dataTables.min.css"'])

__all__ = ['__version__', 'show']
