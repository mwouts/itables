---
jupytext:
  formats: docs///md:myst,docs/py///py:percent
  notebook_metadata_filter: -jupytext.text_representation.jupytext_version
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
kernelspec:
  display_name: python3
  language: python
  name: python3
---

# Options

## DataTable Options

ITables is a wrapper for the JavaScript DataTables library, which means you can often use DataTables [options](https://datatables.net/options) directly within ITables.

Since ITables simply maps these options to DataTables, we encourage you to consult DataTables’ excellent [documentation](https://datatables.net/) and its extensive collection of [examples](https://datatables.net/examples/index). The DataTables [forum](https://datatables.net/forums/) can also be quite helpful.

A non-exhaustive list of DataTables options, along with their expected types, is provided by `DataTableOptions` in [`itables.typing`](https://github.com/mwouts/itables/blob/main/src/itables/typing.py).

## JavaScript Callbacks

DataTables callbacks can customize the table when it is created or redrawn.
Pass JavaScript functions as `itables.JavascriptFunction` objects, rather than
plain strings or Python functions. For example,
[`headerCallback`](https://datatables.net/reference/option/headerCallback)
can style the header each time the table is drawn:

```{code-cell} ipython3
import pandas as pd

import itables

itables.show(
    pd.DataFrame({"value": [1, 2, 3]}),
    headerCallback=itables.JavascriptFunction(
        """function (thead, data, start, end, display) {
    thead.style.color = 'navy';
}"""
    ),
)
```

Option names are case-sensitive: use `headerCallback`, with a lowercase `b`.
The callback runs in the browser and affects the interactive table. It does
not change the static HTML or Markdown preview.

The following callbacks are documented in ITables' option types. See the linked
DataTables reference for each function's arguments and return value.

| Callbacks | Purpose |
| --- | --- |
| [`createdRow`](https://datatables.net/reference/option/createdRow) | Customize a newly created row. |
| [`headerCallback`](https://datatables.net/reference/option/headerCallback), [`footerCallback`](https://datatables.net/reference/option/footerCallback) | Update the header or footer on each draw. Use `footer=True` to include a footer. |
| [`rowCallback`](https://datatables.net/reference/option/rowCallback) | Customize rows on each draw. |
| [`preDrawCallback`](https://datatables.net/reference/option/preDrawCallback), [`drawCallback`](https://datatables.net/reference/option/drawCallback) | Run before or after drawing the table. |
| [`initComplete`](https://datatables.net/reference/option/initComplete) | Run when initialization finishes. |
| [`infoCallback`](https://datatables.net/reference/option/infoCallback), [`formatNumber`](https://datatables.net/reference/option/formatNumber) | Customize the table summary or displayed numbers. |
| [`stateLoadCallback`](https://datatables.net/reference/option/stateLoadCallback), [`stateSaveCallback`](https://datatables.net/reference/option/stateSaveCallback) | Customize where table state is loaded and saved. |
| [`stateLoadParams`](https://datatables.net/reference/option/stateLoadParams), [`stateLoaded`](https://datatables.net/reference/option/stateLoaded), [`stateSaveParams`](https://datatables.net/reference/option/stateSaveParams) | Inspect or modify saved state. |

You can also set callbacks globally on `itables.options`, for example
`itables.options.headerCallback = itables.JavascriptFunction(...)`.
JavaScript callbacks can be used with `show` and `to_html_datatable`; the
widget, Dash, and Streamlit integrations reject JavaScript code in their options.

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

The check occurs both when you set an option on `itables.options`, and when you pass an option to e.g. `show`.

If you find an option that is useful but undocumented, or if you notice an incorrect type hint, please submit a PR (and consider adding an example to the documentation, too).
