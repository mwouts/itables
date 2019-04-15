# Interactive Tables in Jupyter

Turn pandas DataFrames into interactive tables in both your notebooks and their HTML representation, by simply importing `itables`.

```python
import itables
import world_bank_data as wb
wb.get_countries()
```

This is based on the [datatables](https://datatables.net) plug-in for the jQuery Javascript library.

# Installation

Install the package with

```bash
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
- [IPySheet](https://github.com/QuantStack/ipysheet) by QuantStack

If you are looking for a table component that will fit in Dash applications, see [datatable by Dash](https://github.com/plotly/dash-table/).