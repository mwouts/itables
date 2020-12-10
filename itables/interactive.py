"""Activate the representation of Pandas dataframes as interactive tables"""
import warnings

from .javascript import init_notebook_mode

# We issue a FutureWarning rather than a DeprecationWarning...
# because the DeprecationWarning is not shown in the notebook
warnings.warn(
    """Importing itables.interactive is deprecated.
Please execute instead 'from itables import init_notebook_mode; init_notebook_mode(all_interactive=True)'""",
    FutureWarning,
)

init_notebook_mode(all_interactive=True)
