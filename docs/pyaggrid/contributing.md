# Contributing

PyAgGrid is developed in the [ITables](https://github.com/mwouts/itables)
repository, in the `python/pyaggrid` folder. The
[contributing](../pydatatables/contributing.html) and [developing](../pydatatables/developing.html)
guides of the ITables project apply.

The `show` function renders the HTML template at
`python/pyaggrid/src/pyaggrid/html/aggrid_template.html`, which loads AG Grid
Community as an ES module from a CDN. The Jupyter Widget, Dash and Streamlit
components are built from the JavaScript packages at
`packages/pyaggrid*` (run `npm run build-pyaggrid` in `packages/`).

Contributions are welcome! Some ideas:
- an offline mode for `show`, similar to the one of `pydatatables`
- support for more AG Grid features (grouped column headers for
  MultiIndex columns, custom themes, ...)

Please open an issue at [ITables](https://github.com/mwouts/itables/issues)
to discuss your ideas, or to report a problem.
