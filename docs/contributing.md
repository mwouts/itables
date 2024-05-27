---
jupytext:
  formats: md:myst
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

# Contributing

Thanks for considering making a contribution to ITables. There are
many ways you can help!

## Report an issue

If you see an issue, a possible improvement, or if you can't find
the answer to your question, then you are very welcome to create
an issue on this project. Please provide enough detail so that
we can reproduce the issue.

## Improve the documentation

If you would like to add a new example,
or improve the documentation, feel free to make a pull request!

You can render the documentation locally - see the section on
[Jupyter Book](developing.md#jupyter-book) in the developer guide.

## Give credit to ITables

It's always great to see new stars coming to ITables! <a class="github-button" href="https://github.com/mwouts/itables" data-icon="octicon-star" data-show-count="true"></a>
<script src="https://buttons.github.io/buttons.js"></script>

If you wanted to share a link to ITables and DataTables (no obligation whatsoever), you could use something like this:

```{code-cell}
from IPython.display import HTML, display

display(
    HTML(
        """
Tables displayed with <a href=https://mwouts.github.io/itables/>ITables</a>,
a Python wrapper for <a href=https://datatables.net>DataTables</a>
"""
    )
)
```

## Support DataTables

Allan Jardine, the main developer of DataTables, has done a fantastic work on [DataTables](https://datatables.net/).

If you enjoy his library, you could become a
[supporter](https://datatables.net/supporters/) -
contributions range from 9 to 99$/year before VAT.
Or you could take a subscription for DataTable's [Editor](https://editor.datatables.net)
that ITables might support in the future (please subscribe to [#243](https://github.com/mwouts/itables/issues/243) for updates).

## Develop a new feature

It is generally a good idea to get in touch with us first - e.g.
open an issue and let us know what you'd like to do.

But you can also simply clone the project and test your ideas.
A guide on how to set up a development environment, and how to
run some tests, is available [here](developing.md).
