"""The itables options now live in pydatatables.options

This module *is* pydatatables.options, so setting e.g.
itables.options.maxBytes also updates pydatatables.options.maxBytes.
"""

import sys

import pydatatables.options as _options

sys.modules[__name__] = _options
