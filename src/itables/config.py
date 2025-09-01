"""
The ITables options can be modified through an itables.toml configuration file.

The location of that file can be specified through the ITABLES_CONFIG
environment variable (use an empty string for no config). Otherwise ITables will
look for an itables.toml file in the current directory and its parent
directories, for a tool.itables section in a pyproject.toml file in the
current or parent directories, and then for itables.toml in the user config directory.
"""

import os
from itertools import chain
from pathlib import Path
from typing import Any, Optional, cast

try:
    import tomllib
except ImportError:
    try:
        import tomli as tomllib  # pyright: ignore[reportMissingImports]
    except ImportError:
        tomllib = None  # type: ignore[assignment]

try:
    from platformdirs import user_config_path
except ImportError:
    user_config_path = None

from itables.typing import ITableOptions, check_itable_arguments


def get_config_file(path: Path = Path.cwd()) -> Optional[Path]:
    """Return the itables config file if found"""
    if (config_file := os.getenv("ITABLES_CONFIG")) is not None:
        if not config_file:
            # Setting ITABLES_CONFIG to an empty string
            # disables config file loading
            return None

        config_file = Path(config_file)
        if not config_file.exists():
            raise FileNotFoundError(
                f"ITables config file was not found: ITABLES_CONFIG={config_file}"
            )
        return config_file

    ceiling_directories = {
        Path(path)
        for path in os.getenv("ITABLES_CEILING_DIRECTORIES", "").split(":")
        if path
    }
    for parent in chain([path], path.parents):
        config_file = parent / "itables.toml"
        if config_file.exists():
            return config_file
        config_file = parent / "pyproject.toml"
        if config_file.exists():
            with open(config_file, "rb") as fp:
                if tomllib is None:
                    continue
                config = tomllib.load(fp)
                if "tool" not in config or "itables" not in config["tool"]:
                    continue
            return config_file
        if parent in ceiling_directories:
            break

    if user_config_path is not None:
        config_file = user_config_path("itables") / "itables.toml"
        if config_file.exists():
            return config_file

    return None


def load_config_file(config_file: Path) -> ITableOptions:
    if tomllib is None:
        raise ImportError(
            f"Either tomllib or tomli is required to load {config_file}. "
            "Install with 'pip install itables[config]' to enable TOML config support."
        )

    with open(config_file, "rb") as fp:
        try:
            config = tomllib.load(fp)
        except tomllib.TOMLDecodeError as e:
            raise ValueError(f"Failed to load ITables config from {config_file}: {e}")

    if config_file.name == "pyproject.toml":
        if "tool" not in config or "itables" not in config["tool"]:
            raise ValueError(
                f"This pyproject.toml file has no tool.itables section: {config_file}"
            )
        config = config["tool"]["itables"]

    try:
        check_itable_arguments(config, ITableOptions)
    except ValueError as e:
        raise ValueError(f"Invalid ITables config in {config_file}: {e}")
    return cast(ITableOptions, config)


def set_options_from_config_file(options: dict[str, Any]) -> None:
    if (config_file := get_config_file()) is not None:
        config = load_config_file(config_file)
        for key, value in config.items():
            options[key] = value
