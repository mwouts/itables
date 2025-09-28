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

You can also change the default options for all your notebooks and applications by creating an `itables.toml` [configuration file](../configuration.md).


## Option Names and Type Checks

Option names and types are checked by default at runtime when `typeguard>=4.4.1` is installed. You can disable this by setting `warn_on_undocumented_option=False`.

If you find an option that is useful but undocumented, or if you notice an incorrect type hint, please submit a PR (and consider adding an example to the documentation, too).
