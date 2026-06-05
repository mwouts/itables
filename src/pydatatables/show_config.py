"""
Show the location and content of the PyDataTablesRenderers config file.

python -m pydatatables.show_config
"""

from pathlib import Path

from pydatatables.config import get_config_file, load_config_file, tomllib, user_config_path


def show_config(path: Path):
    """
    Show the PyDataTablesRenderers config file location and content.
    """
    if (tomllib is None) or (user_config_path is None):
        print(
            "Missing pydatatables[config] dependencies. Please install them with 'pip install pydatatables[config]'"
        )
        return

    if (config_file := get_config_file(path)) is None:
        print("No PyDataTablesRenderers config file found")
        return

    print(f"PyDataTablesRenderers config file: {config_file}")
    config = load_config_file(config_file)
    print("PyDataTablesRenderers options:")
    for key, value in config.items():
        print(f"  {key}: {value}")


if __name__ == "__main__":
    show_config(Path.cwd())
