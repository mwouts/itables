"""The itables config module now lives in pydatatables.config

Note: the configuration file is now named pydatatables.toml (was itables.toml),
the pyproject.toml section is [tool.pydatatables] (was [tool.itables]), and the
environment variables are PYDATATABLES_CONFIG and PYDATATABLES_CEILING_DIRECTORIES.
"""

import sys

import pydatatables.config as _config

sys.modules[__name__] = _config
