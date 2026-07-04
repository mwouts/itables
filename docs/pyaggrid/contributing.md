# Contributing

PyAgGrid is developed in the [ITables](https://github.com/mwouts/itables)
repository, in the `python/pyaggrid` folder. The
[contributing](../pydatatables/contributing.html) and [developing](../pydatatables/developing.html)
guides of the ITables project apply.

Compared to `pydatatables`, the `pyaggrid` package is younger and simpler:
it has no JavaScript build step - the HTML template at
`python/pyaggrid/src/pyaggrid/html/aggrid_template.html` loads AG Grid
Community as an ES module from a CDN.

Contributions are welcome! Some ideas:
- an offline mode, similar to the one of `pydatatables`
- native Jupyter Widget, Dash, Streamlit or Shiny components
- support for more AG Grid features (grouped column headers for
  MultiIndex columns, custom themes, ...)

Please open an issue at [ITables](https://github.com/mwouts/itables/issues)
to discuss your ideas, or to report a problem.
