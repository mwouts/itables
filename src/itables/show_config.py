"""
Show the location and content of the ITables config file.

python -m itables.show_config
"""

from pathlib import Path

from itables.config import get_config_file, load_config_file


def show_config(path: Path):
    """
    Show the ITables config file location and content.
    """
    if (config_file := get_config_file(path)) is None:
        print("No ITables config file found")
        return

    print(f"ITables config file: {config_file}")
    config = load_config_file(config_file)
    print("ITables options:")
    for key, value in config.items():
        print(f"  {key}: {value}")


if __name__ == "__main__":
    show_config(Path.cwd())
