ITables ChangeLog
=================

1.1.0 (2022-06-23)
------------------

**Added**
- `itables.options` and the `show` function have a new `column_filters` argument to display individual column search boxes ([#69](https://github.com/mwouts/jupytext/issues/69))
- We have documented DataTables' `dom` option.
- We have introduced a new class `JavascriptFunction` to limit the evaluation of Javascript function to selected ones.
- The documentation is formatted with `black` thanks to a Jupytext & Black pre-commit hook.


1.0.0 (2022-06-22)
------------------

**Added**
- ITables works offline! ([#8](https://github.com/mwouts/jupytext/issues/8), [#70](https://github.com/mwouts/jupytext/issues/70)). Marc would like to thank
[Allan Jardine](https://sprymedia.co.uk/), the author of the [datatables](https://datatables.net/) library,
and [François Wouts](https://github.com/fwouts) for their precious help on the subject.


**Changed**
- ITables uses the ESM version 1.12.1 of datatables.net


0.4.7 (2022-04-13)
------------------

**Added**
- Additional `tags` like e.g. captions are supported ([#10](https://github.com/mwouts/jupytext/issues/10)).


0.4.6 (2022-03-29)
------------------

**Changed**
- We have removed the default column width at 70 pixels ([#61](https://github.com/mwouts/jupytext/issues/61), [#62](https://github.com/mwouts/jupytext/issues/62), [#66](https://github.com/mwouts/jupytext/issues/66))
- We now use `pyupgrade` in our pre-commit hooks

**Fixed**
- We have improved the rendering of multiindex columns ([#63](https://github.com/mwouts/jupytext/issues/63))


0.4.5 (2022-01-25)
------------------

**Changed**
- The `itables` documentation now uses Jupyter Book ([#56](https://github.com/mwouts/jupytext/issues/56))
- We have added a new `style` option in `itables.options` and in `show`, with a default value equal to `max-width:100%`.


0.4.4 (2022-01-10)
------------------

**Fixed**
- Add 'require_config.js' to the pip package ([#48](https://github.com/mwouts/jupytext/issues/48))


0.4.3 (2022-01-08)
------------------

**Changed**
- When a JS function is created on the Python side, we export it as-is (without quotes) in the HTML file and don't use JS eval anymore.


0.4.2 (2022-01-07)
------------------

**Fixed**
- Fix the HTML output when `eval_functions=True`
- Display "Loading..." under the table header until the table is displayed with datatables.net
- `init_notebook_mode(all_interactive=False)` restores the original Pandas HTML representation.

0.4.1 (2022-01-06)
------------------

**Fixed**
- Long column names don't overlap anymore ([#28](https://github.com/mwouts/jupytext/issues/28))


0.4.0 (2022-01-06)
------------------

r**Fixed**
- Now `itables` also works in Jupyter Lab, Colab, VS Code and PyCharm ([#3](https://github.com/mwouts/jupytext/issues/3), [#4](https://github.com/mwouts/jupytext/issues/4), [#26](https://github.com/mwouts/jupytext/issues/26), [#40](https://github.com/mwouts/jupytext/issues/40)), as we load the `datatables.net` library with an ES import when `require.js` is not available. Many thanks to [François Wouts](https://github.com/fwouts) for his precious help!

**Changed**
- The `show` function (and `itables.options`) has a new argument `eval_functions`. When set to `True`, the nested strings passed to `datatables.net` that start with `function` are converted to Javascript functions.
- The HTML code for the datatables.net representation of the table is generated with an HTML template.
- We use f-strings and thus require Python >= 3.6


0.3.1 (2021-12-24)
------------------

**Fixed**
- We fixed an issue (`jquery` not found) with the HTML export when using `nbconvert>=6.0` ([#21](https://github.com/mwouts/jupytext/issues/21))
- We documented how to change the default ordering of rows - with the `order` option ([#30](https://github.com/mwouts/jupytext/issues/30))
- We documented how to load `require` in Jupyter Lab ([#3](https://github.com/mwouts/jupytext/issues/3))

**Changed**
- The main branch for the project is `main` rather than `master`
- Updated `datatables` to 1.11.3 and `jquery` to 3.5.1


0.3.0 (2020-12-14)
------------------

**Fixed**
- `itables` now has an explicit `init_notebook_mode` function, which inserts the datatables.net library in the notebook. Use `init_notebook_mode(all_interactive=True)` to display all the pandas object as interactive tables. This fixes ([#6](https://github.com/mwouts/jupytext/issues/6)) and ([#17](https://github.com/mwouts/jupytext/issues/17)).

**Changed**
- `itables` uses GitHub Actions for the CI.

**Added**
- `itables` is tested with Python 3.9 as well.


0.2.2 (2020-10-01)
------------------

**Fixed**
- Pandas' `display.max_columns` can be `None`, by Arthur Deygin ([#14](https://github.com/mwouts/jupytext/issues/14))


0.2.1 (2019-11-21)
------------------

**Added**
- Animated screenshot in README

**Fixed**
- Add IPython to setup.py install_requires, by Jon Shao ([#9](https://github.com/mwouts/jupytext/issues/9))


0.2.0 (2019-11-20)
------------------

**Added**
- Large tables are downsampled ([#2](https://github.com/mwouts/jupytext/issues/2))

**Changed**
- Javascript code moved to Javascript files

**Fixed**
- Tables with many columns are now well rendered ([#5](https://github.com/mwouts/jupytext/issues/5))


0.1.0 (2019-04-23)
------------------

Initial release
