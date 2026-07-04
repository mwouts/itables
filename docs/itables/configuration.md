---
jupytext:
  formats: docs///md:myst,docs/py///py:percent
  notebook_metadata_filter: -jupytext.text_representation.jupytext_version
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
kernelspec:
  display_name: itables
  language: python
  name: itables
---

# Configuration

ITables exposes many of the `datatables` [options](options/options.md). Since ITables v2.5, the default values for these options can be set in an `itables.toml` configuration file.

## Prerequisites

You will need ITables v2.5 or higher, and two dependencies: either `tomllib` or `tomli`, and `platformdirs`, which can be installed with `pip install itables[config]`.

## Configuration file

The configuration file is identified using `get_config_file` from [`itables.config`](https://github.com/mwouts/itables/blob/main/src/itables/config.py). It can be:

- The file pointed to by the environment variable `ITABLES_CONFIG`, if set and non-empty (if the variable is an empty string, no configuration file is used)
- An `itables.toml` file in the current directory or a parent directory
- A `tool.itables` section in a `pyproject.toml` file in the current directory or a parent directory

## Example configuration

A simple `itables.toml` configuration file that makes the tables less [compact](options/classes.md) looks like this:
```
classes = ["display", "nowrap"]
```

If you want the Excel export button on each table, add this:
```
buttons = ["pageLength", "copyHtml5", "csvHtml5", "excelHtml5"]
```

And if you want to use the [column control](options/column_control.md) extension:
```
[[columnControl]]
target = 0
content = ["order"]
[[columnControl]]
target = "tfoot"
content = ["search"]

[ordering]
indicators = false
handler = false
```

## Modifying the configuration

The configuration file is loaded when `itables` is imported. If you make changes to the configuration file, these will take effect only when you restart Python and re-import ITables.

You can confirm which configuration file is being used (in a given directory) by running:
```
python -m itables.show_config
```
