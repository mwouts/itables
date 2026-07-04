"""The itables.utils module now lives in pydatatables.utils"""

import sys

import pydatatables.utils as _utils

sys.modules[__name__] = _utils
