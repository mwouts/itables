# Shiny

You can use ITables in Web applications generated with [Shiny](https://shiny.rstudio.com/py/) for Python with e.g.
```python
from shiny import ui

from itables.sample_dfs import get_countries
from itables.shiny import DT

df = get_countries(html=False)
ui.HTML(DT(df))
```

See also our [tested examples](https://github.com/mwouts/itables/tree/main/tests/sample_python_apps).
