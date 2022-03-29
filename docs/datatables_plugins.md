---
jupytext:
  formats: md:myst,ipynb
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.11.5
kernelspec:
  display_name: itables
  language: python
  name: itables
---

# DataTables Plugins

As always, we initialize the `itables` library with

```{code-cell} ipython3
from itables import init_notebook_mode, show

init_notebook_mode(all_interactive=True)
```

and we load a sample dataframe

```{code-cell} ipython3
from itables.sample_dfs import get_countries

df = get_countries()
```

## Copy, CSV, PDF and Excel buttons

TODO: Here I'd like to port the official [buttons example](https://datatables.net/extensions/buttons/examples/html5/simple.html)

```{code-cell} ipython3
import itables.options as opt

opt.requirements = [
    "https://code.jquery.com/jquery-3.5.1.js",
    "https://cdn.datatables.net/1.11.5/js/jquery.dataTables.min.js",
    "https://cdn.datatables.net/buttons/2.2.2/js/dataTables.buttons.min.js",
    "https://cdnjs.cloudflare.com/ajax/libs/jszip/3.1.3/jszip.min.js",
    "https://cdnjs.cloudflare.com/ajax/libs/pdfmake/0.1.53/pdfmake.min.js",
    "https://cdnjs.cloudflare.com/ajax/libs/pdfmake/0.1.53/vfs_fonts.js",
    "https://cdn.datatables.net/buttons/2.2.2/js/buttons.html5.min.js"]

show(df, buttons= [
            'copyHtml5',
            'excelHtml5',
            'csvHtml5',
            'pdfHtml5'
        ])
```

## Search Highlighting

TODO: Here I'd like to provide an example of search highlighting

```{code-cell} ipython3
import itables.options as opt

opt.requirements = ["https://cdn.jsdelivr.net/npm/jquery@3.5.1/dist/jquery.min.js",
                    "https://cdn.datatables.net/1.11.5/js/jquery.dataTables.min.js",
                    "https://cdn.jsdelivr.net/mark.js/8.6.0/jquery.mark.min.js",
                    "https://cdn.jsdelivr.net/datatables.mark.js/2.0.0/datatables.mark.min.js"
                   ]

df
```
