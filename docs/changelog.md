ITables ChangeLog
=================

1.3.5 (2022-11-12)
------------------

**Fixed**
- We use `pandas.io.formats.format.format_array` to format non-trivial dtypes (as in `itables<=1.3.1`) ([#112](https://github.com/mwouts/itables/issues/112))
- The downsampling of large tables is faster. We have also added a new function `generate_random_df` to generate large tables on demand ([#113](https://github.com/mwouts/itables/issues/113))
- We don't raise a warning anymore when a table is downsampled. Instead, we add this information to the table summary ([#114](https://github.com/mwouts/itables/issues/114))

**Added**
- We have added support for Python 2 ([#115](https://github.com/mwouts/itables/issues/115)).


1.3.4 (2022-11-07)
------------------

**Fixed**
- We have removed `scrollX = True` which was causing issues with non-wide tables ([#110](https://github.com/mwouts/itables/issues/110)). Instead, we now use `style = "width:auto"`.


1.3.3 (2022-11-06)
------------------

**Changed**
- We have added `scrollX = True` to the default options to make the rendering of wide tables more similar to Pandas.


1.3.2 (2022-11-06)
------------------

**Fixed**
- We have reimplemented the function that encodes the Pandas dataframes to JSON
to avoid triggering FutureWarnings when using `pandas>=1.5` ([#107](https://github.com/mwouts/itables/issues/107)).


1.3.1 (2022-11-05)
------------------

**Added**
- The `show` method has a new `css` argument (defaults to `itables.options.css`) ([#104](https://github.com/mwouts/itables/issues/104)).


1.3.0 (2022-09-04)
------------------

**Changed**
- The order of rows is preserved by default (unless you explicitly pass an `order` parameter) ([#99](https://github.com/mwouts/itables/issues/99)).

**Fixed**
- Nullable types (bool, int) are now supported ([#98](https://github.com/mwouts/itables/issues/98))


1.2.0 (2022-08-15)
------------------

**Added**
- New `to_html_datatable` function to export a DataFrame to an HTML div ([#88](https://github.com/mwouts/itables/issues/88))
- We have added examples on how to use `itables` in [Shiny](https://shiny.rstudio.com/py/) for Python ([#86](https://github.com/mwouts/itables/issues/86))


1.1.3 (2022-08-11)
------------------

**Fixed**
- Tables with duplicated column names are now supported, thanks to Antonio Commisso's fix ([#89](https://github.com/mwouts/itables/issues/89))


1.1.2 (2022-06-30)
------------------

**Changed**
- Tables with many rows are preferentially downsampled on rows, while tables with many columns are preferentially downsampled on columns ([#84](https://github.com/mwouts/itables/issues/84))


1.1.1 (2022-06-23)
------------------

**Fixed**
- Added missing `column_filters` package data.


1.1.0 (2022-06-23)
------------------

**Added**
- `itables.options` and the `show` function have a new `column_filters` argument to display individual column search boxes ([#69](https://github.com/mwouts/itables/issues/69))
- We have documented DataTables' `dom` option.
- We have introduced a new class `JavascriptFunction` to limit the evaluation of Javascript function to selected ones.
- The documentation is formatted with `black` thanks to a Jupytext & Black pre-commit hook.


1.0.0 (2022-06-22)
------------------

**Added**
- ITables works offline! ([#8](https://github.com/mwouts/itables/issues/8), [#70](https://github.com/mwouts/itables/issues/70)). Marc would like to thank
[Allan Jardine](https://sprymedia.co.uk/), the author of the [datatables](https://datatables.net/) library,
and [François Wouts](https://github.com/fwouts) for their precious help on the subject.


**Changed**
- ITables uses the ESM version 1.12.1 of datatables.net


0.4.7 (2022-04-13)
------------------

**Added**
- Additional `tags` like e.g. captions are supported ([#10](https://github.com/mwouts/itables/issues/10)).


0.4.6 (2022-03-29)
------------------

**Changed**
- We have removed the default column width at 70 pixels ([#61](https://github.com/mwouts/itables/issues/61), [#62](https://github.com/mwouts/itables/issues/62), [#66](https://github.com/mwouts/itables/issues/66))
- We now use `pyupgrade` in our pre-commit hooks

**Fixed**
- We have improved the rendering of multiindex columns ([#63](https://github.com/mwouts/itables/issues/63))


0.4.5 (2022-01-25)
------------------

**Changed**
- The `itables` documentation now uses Jupyter Book ([#56](https://github.com/mwouts/itables/issues/56))
- We have added a new `style` option in `itables.options` and in `show`, with a default value equal to `max-width:100%`.


0.4.4 (2022-01-10)
------------------

**Fixed**
- Add 'require_config.js' to the pip package ([#48](https://github.com/mwouts/itables/issues/48))


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
- Long column names don't overlap anymore ([#28](https://github.com/mwouts/itables/issues/28))


0.4.0 (2022-01-06)
------------------

r**Fixed**
- Now `itables` also works in Jupyter Lab, Colab, VS Code and PyCharm ([#3](https://github.com/mwouts/itables/issues/3), [#4](https://github.com/mwouts/itables/issues/4), [#26](https://github.com/mwouts/itables/issues/26), [#40](https://github.com/mwouts/itables/issues/40)), as we load the `datatables.net` library with an ES import when `require.js` is not available. Many thanks to [François Wouts](https://github.com/fwouts) for his precious help!

**Changed**
- The `show` function (and `itables.options`) has a new argument `eval_functions`. When set to `True`, the nested strings passed to `datatables.net` that start with `function` are converted to Javascript functions.
- The HTML code for the datatables.net representation of the table is generated with an HTML template.
- We use f-strings and thus require Python >= 3.6


0.3.1 (2021-12-24)
------------------

**Fixed**
- We fixed an issue (`jquery` not found) with the HTML export when using `nbconvert>=6.0` ([#21](https://github.com/mwouts/itables/issues/21))
- We documented how to change the default ordering of rows - with the `order` option ([#30](https://github.com/mwouts/itables/issues/30))
- We documented how to load `require` in Jupyter Lab ([#3](https://github.com/mwouts/itables/issues/3))

**Changed**
- The main branch for the project is `main` rather than `master`
- Updated `datatables` to 1.11.3 and `jquery` to 3.5.1


0.3.0 (2020-12-14)
------------------

**Fixed**
- `itables` now has an explicit `init_notebook_mode` function, which inserts the datatables.net library in the notebook. Use `init_notebook_mode(all_interactive=True)` to display all the pandas object as interactive tables. This fixes ([#6](https://github.com/mwouts/itables/issues/6)) and ([#17](https://github.com/mwouts/itables/issues/17)).

**Changed**
- `itables` uses GitHub Actions for the CI.

**Added**
- `itables` is tested with Python 3.9 as well.


0.2.2 (2020-10-01)
------------------

**Fixed**
- Pandas' `display.max_columns` can be `None`, by Arthur Deygin ([#14](https://github.com/mwouts/itables/issues/14))


0.2.1 (2019-11-21)
------------------

**Added**
- Animated screenshot in README

**Fixed**
- Add IPython to setup.py install_requires, by Jon Shao ([#9](https://github.com/mwouts/itables/issues/9))


0.2.0 (2019-11-20)
------------------

**Added**
- Large tables are downsampled ([#2](https://github.com/mwouts/itables/issues/2))

**Changed**
- Javascript code moved to Javascript files

**Fixed**
- Tables with many columns are now well rendered ([#5](https://github.com/mwouts/itables/issues/5))


0.1.0 (2019-04-23)
------------------

Initial release
