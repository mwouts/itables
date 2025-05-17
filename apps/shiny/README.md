# ITables in Shiny for Python: a Demo

This directory contains two example Python for Shiny applications that render
Pandas DataFrames using [ITables](https://mwouts.github.io/itables).

## The ITable Widget

This is the recommended way to use ITable in a Shiny application.

See the source code at [`app.py`](itable_widget/app.py) (Shiny Express) or [`app-core.py`](itable_widget/app-core.py) (Shiny Core).

Install the requirements with
```
pip install -r itable_widget/requirements.txt
```
and launch the app with
```
shiny run itable_widget/app-express.py  # or app-core.py
```

Or access the app online at https://itables.shinyapps.io/itable_widget/

## Using DT

This is an alternative way to use ITable in a Shiny application.

See the source code at [`app.py`](itables_DT/app.py) (Shiny Express) or [`app-core.py`](itables_DT/app-core.py) (Shiny Core).

Install the requirements with
```
pip install -r itables_DT/requirements.txt
```
and launch the app with
```
shiny run itables_DT/app-express.py  # or app-core.py
```

Or access the app online at https://itables.shinyapps.io/itables_DT/
