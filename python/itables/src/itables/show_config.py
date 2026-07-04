"""
Show the location and content of the config file.

python -m itables.show_config
"""

from pathlib import Path

from pydatatables.show_config import show_config  # noqa: F401

if __name__ == "__main__":
    show_config(Path.cwd())
