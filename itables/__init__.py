from .javascript import show, load_datatables, init_itables
from .version import __version__

load_datatables()

__all__ = ['__version__', 'show', 'init_itables']
