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

# Options

## DataTable Options

ITables is a wrapper for the JavaScript DataTables library, which means you can often use DataTables [options](https://datatables.net/options) directly within ITables.

Since ITables simply maps these options to DataTables, we encourage you to consult DataTables’ excellent [documentation](https://datatables.net/) and its extensive collection of [examples](https://datatables.net/examples/index). The DataTables [forum](https://datatables.net/forums/) can also be quite helpful.

A non-exhaustive list of DataTables options, along with their expected types, is provided by `DataTableOptions` in [`itables.typing`](https://github.com/mwouts/itables/blob/main/src/itables/typing.py).

## ITable Options

ITables adds a few options of its own, such as `connected`, `maxBytes`, `allow_html`, and others. An exhaustive list of these additional options is provided by `ITableOptions` in [`itables.typing`](https://github.com/mwouts/itables/blob/main/src/itables/typing.py).

## Default Values

The default values for these options are set in [`itables.options`](https://github.com/mwouts/itables/blob/main/src/itables/options.py). These defaults are used in each call to `to_html_datatable`, `show`, or `ITable`, unless a corresponding option is set locally—in which case, the local value takes precedence.

## Changing the Defaults

You can change the default options in your notebook or application with:

```python
import itables

itables.options.maxBytes = "128KB"
```

## Configuration File

Since v2.5.0, ITable can load its default options from a configuration file. The configuration file is identified using `get_config_file` from [`itables.config`](https://github.com/mwouts/itables/blob/main/src/itables/config.py). It can be:

- The file pointed to by the environment variable `ITABLES_CONFIG`, if set and non-empty (if the variable is an empty string, no configuration file is used)
- An `itables.toml` file in the current or a parent directory
- A `tool.itables` section in a `pyproject.toml` file in the current or a parent directory

A sample configuration file could look like this:
```
# itables.toml
classes = ["display", "nowrap", "compact"]
buttons = ["pageLength", "copyHtml5", "csvHtml5", "excelHtml5"]
```

Add this to use the [column control](column_control.md) extension:
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

The configuration file is loaded when `itables` is imported - you will need to restart Python and re-import ITables to get the latest configuration.

You can confirm which configuration file is being used (in a given directory) by running
```
python -m itables.show_config
```


## Option Names and Type Checks

Option names and types are checked by default at runtime when `typeguard>=4.4.1` is installed. You can disable this by setting `warn_on_undocumented_option=False`.

If you find an option that is useful but undocumented, or if you notice an incorrect type hint, please submit a PR (and consider adding an example to the documentation, too).
