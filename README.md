# Interactive Tables in Jupyter

[![Build Status](https://travis-ci.com/mwouts/itables.svg?branch=master)](https://travis-ci.com/mwouts/itables)
[![codecov.io](https://codecov.io/github/mwouts/itables/coverage.svg?branch=master)](https://codecov.io/github/mwouts/itables?branch=master)

Turn pandas DataFrames and Series into interactive tables in both your notebooks and their HTML representation, by simply using the `show` function from `itables`. This is based on the [datatables](https://datatables.net) plug-in for the jQuery Javascript library.

```python
from itables import show
import world_bank_data as wb
show(wb.get_countries())
```

![](https://gist.githubusercontent.com/mwouts/165badb3f8ab345a25739a792859583b/raw/43d66231a1f916b350d266a8cb503dd30d7ae1e2/datatables.png)

Note that if you want to display every dataframe or series as an interactive table, you just need to `import itables.interactive`.

```python
import itables.interactive
wb.get_series('SP.POP.TOTL', mrv=1, simplify_index=True)
```

# Installation

Install the package with

```bash active=""
pip install itables
```

# References

## DataTables

- DataTables is a plug-in for the jQuery Javascript library. It has a great [documentation](https://datatables.net/manual/), and a large set of [examples](https://datatables.net/examples/index).
- The R package [DT](https://rstudio.github.io/DT/) uses datatables.net as the underlying library for both R notebooks, and Shiny applications. In addition to the standard datatables.net library, RStudio seems to have implemented cell edition, and row selection.
- Marek Cermak has an interesting [tutorial](https://medium.com/@marekermk/guide-to-interactive-pandas-dataframe-representation-485acae02946) on how to use datatables.net within Jupyter, and he also published [jupyter-datatables](https://github.com/CermakM/jupyter-datatables), with interesting distribution plots when the data is numerical.

## Going further

ITables is not a Jupyter widget, which means that it does not allows you to **edit** the content of the dataframe. 
If you are looking for more interactivity, have a look at
- [QGrid](https://github.com/quantopian/qgrid) by Quantopian
- [IPyaggrid](https://dgothrek.gitlab.io/ipyaggrid/) by Louis Raison and Olivier Borderies
- [IPySheet](https://github.com/QuantStack/ipysheet) by QuantStack

If you are looking for a table component that will fit in Dash applications, see [datatable by Dash](https://github.com/plotly/dash-table/).