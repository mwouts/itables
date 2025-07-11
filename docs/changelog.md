ITables ChangeLog
=================

2.4.4 (2025-07-07)
------------------

**Fixed**
- We have fixed an assertion error when a `table_id` argument is passed to `DT` ([#417](https://github.com/mwouts/itables/issues/417))


2.4.3 (2025-07-01)
------------------

**Fixed**
- We have fixed an issue with an index not shown when `polars` was not installed ([#415](https://github.com/mwouts/itables/issues/415))


2.4.2 (2025-06-11)
------------------

**Added**
- We have added a `Framework :: Dash` classifier to highlight the fact that ITables has a component for Dash
- We have added more type annotations ([#390](https://github.com/mwouts/itables/issues/390))

**Fixed**
- We have added a `Typing :: Typed` classifier to the package as ITables now comes with type annotations ([#411](https://github.com/mwouts/itables/issues/411))
- Added type hints and an example for `pageLength` ([#410](https://github.com/mwouts/itables/issues/410))


2.4.1 (2025-06-10)
------------------

**Added**
- We enforce strict `pyright` on the ITables documentation ([#395](https://github.com/mwouts/itables/issues/395)) and on the example apps ([#401](https://github.com/mwouts/itables/pull/401))

**Changed**
- The `warn_on_undocumented_option` option now defaults to `True` and only check the option names
- We have added a new option `warn_on_unexpected_option_type` that defaults to `warn_on_undocumented_option` when `typeguard>=4.4.1` is installed (`False` otherwise)
- Wrapping JS function definitions in parentheses prior to JS eval is now done on the JS side.

**Fixed**
- We have added type hints to `itable.options` even for the options that don't have a default value ([#224](https://github.com/mwouts/itables/issues/224))
- The optional final semicolon in `style` argument is now supported again ([#386](https://github.com/mwouts/itables/issues/386))
- The index of Pandas Style object is now rendered when non-trivial ([#393](https://github.com/mwouts/itables/issues/393))
- We have made the CSS files compatible with the shadow dom used by Marimo ([#383](https://github.com/mwouts/itables/issues/383))
- A workaround for the incorrect widget weight in Shiny is to use `fillable=False` in the `output_widget` ([#360](https://github.com/mwouts/itables/issues/360))
- We have fixed a Javascript error in the Jupyter widget ('t.state_change is undefined') ([#407](https://github.com/mwouts/itables/issues/407))


2.4.0 (2025-05-17)
------------------

**Added**
- The ITable widget, and the ITable components for Dash and Streamlit have the same features as the `show` function. They can show non-finite floats, bigints, Pandas Style objects and use custom JavaScript formatters ([#374](https://github.com/mwouts/itables/issues/374))
- We have added type hints for the `show` function and for the various app components. A SyntaxWarning is issued if either the argument name or type does not match when `warn_on_undocumented_option=True` (the default when `typeguard>=4.4.1` is installed)
- We have added more application examples, and documented how to use ITables in Marimo ([#348](https://github.com/mwouts/itables/issues/348))

**Changed**
- By default, the HTML content in Pandas and Polars dataframes is now escaped. Use `allow_html=True` to display HTML content (use this option only if you trust the content of the table!) ([#346](https://github.com/mwouts/itables/issues/346))
- Consistently with Pandas Style, the HTML content in Styler objects is not escaped - make sure you trust the content of the corresponding tables.
- We have updated DataTables to its latest release 2.3.0
- ITable now requires Python 3.9, due to the addition of type hints
- The `dom` argument (deprecated in v2.0) has been removed.

**Fixed**
- We have added a new option `text_in_header_can_be_selected` (defaults to `True`). With that option the text in headers can be selected, giving you the option to select and copy the column names back to your Python code.
- We have fixed the rendering of Polars Struct columns ([#290](https://github.com/mwouts/itables/issues/290))


2.3.0 (2025-04-05)
------------------

**Added**
- ITable now has a component for Dash! You can render your Python DataFrames in your Dash application with `from itables.dash import ITable` ([#245](https://github.com/mwouts/itables/issues/245))

**Changed**
- We have changed the default value of the `all_interactive` argument of `itables.init_notebook_mode` to `True`
- The ITables options can be imported and modified directly through `itables.options`
- We have updated `dt_for_itables` to `datatables.net-dt==2.2.2` and `datatables.net-select-dt==3.0.0`
- We have updated the dependencies of our Jupyter widget and our of Streamlit component.


2.2.5 (2025-02-22)
------------------

**Fixed**
- We have removed an erroneous assertion and added tests on the warnings issued when selected rows are not displayed ([[#351](https://github.com/mwouts/itables/issues/351)])


2.2.4 (2024-12-07)
------------------

**Fixed**
- We have fixed an issue with the HTML export of multiple tables in the same cell ([#338](https://github.com/mwouts/itables/issues/338))
- The dependencies of the Streamlit component have been updated ([#343](https://github.com/mwouts/itables/pull/343), [#345](https://github.com/mwouts/itables/pull/345))


2.2.3 (2024-11-01)
------------------

**Fixed**
- Table footers continue to work when the notebook is exported to HTML ([#331](https://github.com/mwouts/itables/issues/331))
- The dependencies of the Streamlit component have been updated ([#327](https://github.com/mwouts/itables/pull/327), [#330](https://github.com/mwouts/itables/pull/330))

**Added**
- ITables is now tested with Python 3.13


2.2.2 (2024-09-29)
------------------

**Fixed**
- We have fixed a HTML pop up warning when displaying Pandas Style objects in Quarto ([#317](https://github.com/mwouts/itables/issues/317))
- The dependencies of the Streamlit component have been updated ([#323](https://github.com/mwouts/itables/pull/323))

**Added**
- We have documented how to use the `ITable` widget in a Shiny application
- We have deployed a sample Shiny app ([#276](https://github.com/mwouts/itables/issues/276))


2.2.1 (2024-09-22)
------------------

**Fixed**
- We fixed an issue with the Streamlit component when `selected_rows` was not set.


2.2.0 (2024-09-22)
------------------

**Added**
- ITables has a Jupyter Widget ([#267](https://github.com/mwouts/itables/issues/267)). Our widget was developed and packaged using [AnyWidget](https://anywidget.dev/) which I highly recommend!
- The selected rows are now available in the apps. Use either the `selected_rows` attribute of the `ITable` widget, the returned value of the Streamlit `interactive_table` component, or the `{table_id}_selected_rows` input in Shiny ([#208](https://github.com/mwouts/itables/issues/208), [#250](https://github.com/mwouts/itables/issues/250))
- ITables works offline in Shiny applications too - just add `ui.HTML(init_itables())` to your application

**Changed**
- The `tableId` argument of `to_html_datatable` has been renamed to `table_id`

**Fixed**
- The dependencies of the Streamlit component have been updated ([#320](https://github.com/mwouts/itables/issues/320))


2.1.5 (2024-09-08)
------------------

**Fixed**
- DataTables was updated to its latest version (2.1.6)
- We have added the DateTime extension, required by SearchTime when showing dates ([#288](https://github.com/mwouts/itables/issues/288))
- We have improved the function that determines whether a dark theme is being used ([#294](https://github.com/mwouts/itables/issues/294))
- We have adjusted the generation of the Polars sample dataframes to fix the CI ([Polars-18130](https://github.com/pola-rs/polars/issues/18130))
- The test on the Shiny app fallbacks to `ui.nav_panel` when `ui.nav` is not available
- The dependencies of the Streamlit component have been updated ([#313](https://github.com/mwouts/itables/issues/313), [#315](https://github.com/mwouts/itables/issues/315))


2.1.4 (2024-07-03)
------------------

**Fixed**
- We have fixed an OverflowError (_can't convert negative int to unsigned_) when displaying Polars DataFrames that contain unsigned integers ([#299](https://github.com/mwouts/itables/issues/299))


2.1.3 (2024-06-22)
------------------

**Fixed**
- We have improved the detection of large integers in the context of Polars DataFrames ([#291](https://github.com/mwouts/itables/issues/291))


2.1.2 (2024-06-19)
------------------

**Changed**
- The default CSS contains now has `overflow:auto` on `div.dt-layout-table>div`. Thanks to this we now get
an automatic horizontal scrolling in Jupyter, Jupyter Book and also Streamlit if the table is too wide ([#282](https://github.com/mwouts/itables/pull/282)).

**Fixed**
- The dependencies of the Streamlit components have been updated to fix a vulnerability in `ws` ([Alert 1](https://github.com/mwouts/itables/security/dependabot/1))


2.1.1 (2024-06-08)
------------------

**Fixed**
- We have added an explicit `encoding` argument in the calls to `read_text` to address an issue seen on Windows ([#252](https://github.com/mwouts/itables/issues/252)).
- We have adjusted the codecov settings ([#280](https://github.com/mwouts/itables/pull/280))

**Changed**
- We have added a default css on `dt-container` equal to `{max-width:100%}`.
- We have updated `datatables.net-dt` to `2.0.8`, and included the [column visibility button](https://datatables.net/extensions/buttons/examples/column_visibility/simple.html) in the `dt_for_itables` package ([#284](https://github.com/mwouts/itables/issues/284))


2.1.0 (2024-05-27)
------------------

**Added**
- ITables works with Streamlit ([#270](https://github.com/mwouts/itables/pull/270))

**Changed**
- ITables now uses the `src` layout ([#246](https://github.com/mwouts/itables/issues/246)) - many thanks to [Mahendra Paipuri](https://github.com/mahendrapaipuri) for his help on this topic!
- We have updated `dt_for_itables`' dependencies to `datatables.net-dt==2.0.7` and `datatables.net-select-dt==2.0.2` ([#273](https://github.com/mwouts/itables/pull/273))
- We have updated the pre-commit hooks used in the project ([#268](https://github.com/mwouts/itables/pull/268))


2.0.1 (2024-04-30)
------------------

**Added**
- We have added a logo for ITables ([#257](https://github.com/mwouts/itables/issues/257))
- The _loading_ message gives more information, including the version of ITables and where DataTables is loaded from ([#258](https://github.com/mwouts/itables/issues/258))

**Changed**
- We have updated `DataTables` to `2.0.5` and its extensions to their latest version ([#260](https://github.com/mwouts/itables/issues/260))
- `maxBytes` can now be a string. Its default value remains unchanged at `64KB` ([#239](https://github.com/mwouts/itables/issues/239))

**Fixed**
- We have improve the compatibility with dark themes ([#255](https://github.com/mwouts/itables/issues/255))
- We now enforce non-sparse index when displaying Pandas Style objects with a multiindex ([#254](https://github.com/mwouts/itables/issues/254))
- Export buttons are shown when using `show(df, buttons=...)` on a Pandas Style object ([#259](https://github.com/mwouts/itables/issues/259))
- We have fixed a side effect when using `logging` ([#265](https://github.com/mwouts/itables/issues/265))


2.0.0 (2024-03-16)
------------------

**Added**
- The CSV, Excel and Print buttons are now included ([#50](https://github.com/mwouts/itables/issues/50), [#155](https://github.com/mwouts/itables/issues/155))
- We have included a few other extensions like SearchBuilder and SearchPanes and documented how to add more ([#178](https://github.com/mwouts/itables/issues/178), [#207](https://github.com/mwouts/itables/issues/207), [#208](https://github.com/mwouts/itables/issues/208), [#231](https://github.com/mwouts/itables/issues/231))
- ITables is now tested with Python 3.12

**Changed**
- ITables uses the latest version `2.0.2` of `DataTables` ([#121](https://github.com/mwouts/itables/issues/121))
- Large Python integers are now mapped to JavaScript `BigInt` ([#172](https://github.com/mwouts/itables/issues/172))
- ITables is build using `hatch` and `pyproject.toml`


1.7.1 (2024-03-05)
------------------

**Fixed**
- The select and search box now use a white font in VS Code (dark mode) ([#232](https://github.com/mwouts/itables/issues/232), [#156](https://github.com/mwouts/itables/issues/156), [#103](https://github.com/mwouts/itables/issues/103))

**Added**
- We have added a check to make sure any `tableId` provided by the user is valid ([#233](https://github.com/mwouts/itables/issues/233))


1.7.0 (2024-02-09)
------------------

**Added**
- ITables works well with Quarto. We have added Quarto examples to the documentation. We set `data-quarto-disable-processing="true"` on the tables that are generated with `use_to_html=False` and thus can't be processed by Quarto ([#179](https://github.com/mwouts/itables/issues/179))

**Fixed**
- ITables works when you duplicate a notebook ([#222](https://github.com/mwouts/itables/issues/222))
- We use `df.isetitem(i, ...)` rather than `df.iloc[:,i] = ...` to avoid a warning with Pandas 2.2.0 ([#223](https://github.com/mwouts/itables/issues/223))

**Changed**
- We have changed how datatables.net is loaded. This is expected to improve the VSCode experience ([#216](https://github.com/mwouts/itables/issues/216))
- We have removed legacy Python 2 code.


1.6.4 (2024-02-03)
------------------

**Fixed**
- Complex table footers are now in the correct order ([#219](https://github.com/mwouts/itables/issues/219))
- We have adjusted the test suite for `pandas==2.2.0`
([#223](https://github.com/mwouts/itables/issues/223),
[pandas-57229](https://github.com/pandas-dev/pandas/issues/57229),
[pandas-55080](https://github.com/pandas-dev/pandas/issues/55080))


1.6.3 (2023-12-10)
------------------

**Changed**
- HTML in table columns is supported ([#213](https://github.com/mwouts/itables/issues/213))


1.6.2 (2023-10-07)
------------------

**Fixed**
- We have removed an indirect dependency on `jinja2` caused by the Pandas style objects ([#202](https://github.com/mwouts/itables/issues/202))


1.6.1 (2023-10-01)
------------------

**Fixed**
- We have fixed an issue when rendering Pandas style objects in Google Colab ([#199](https://github.com/mwouts/itables/issues/199))


1.6.0 (2023-09-30)
------------------

**Added**
- We have added support for [Pandas style](https://pandas.pydata.org/docs/user_guide/style.html) ([#194](https://github.com/mwouts/itables/issues/194))

**Fixed**
- We do not generate timedeltas in the sample dataframes when using `pandas==2.1` as this fails ([pandas-55080](https://github.com/pandas-dev/pandas/issues/55080))


1.5.4 (2023-08-18)
------------------

**Fixed**
- Fixed an OverflowError when displaying Polar tables containing unsigned integers ([#192](https://github.com/mwouts/itables/issues/192))

**Changed**
- We have refactored the GitHub Action workflows. Python 2 was removed since it is not supported anymore.


1.5.3 (2023-06-11)
------------------

**Fixed**
- We fixed an interaction issue with other ui elements in Shiny apps - use `from itables.shiny import DT` ([#181](https://github.com/mwouts/itables/issues/181))
- We fixed the rendering of some empty dataframes


1.5.2 (2023-03-26)
------------------

**Fixed**
- Integers that are too big for Javascript are converted to str ([#152](https://github.com/mwouts/itables/issues/152))
- If a downsampling occurs, the downsampling message is displayed even if the table only has a few rows

**Added**
- We have added a CI configuration where we test `itables` against `pandas` in pre-release versions


1.5.1 (2023-03-12)
------------------

**Fixed**
- Empty Polars DataFrame are now rendered correctly ([#167](https://github.com/mwouts/itables/issues/167))


1.5.0 (2023-03-11)
------------------

**Fixed**
- We have addressed the `window.initializeDataTable` is not a function error when a notebook is reloaded
([#160](https://github.com/mwouts/itables/issues/160), [#163](https://github.com/mwouts/itables/issues/163)).
Many thanks again to [François Wouts](https://github.com/fwouts) for providing the right fix!

**Added**
- Polars DataFrames are supported ([#159](https://github.com/mwouts/itables/issues/159))
- We have added an example to show how to include images in tables ([#158](https://github.com/mwouts/itables/issues/158))
- We have added links and images (flags from https://flagpedia.net) to the sample countries df ([#158](https://github.com/mwouts/itables/issues/158)).

**Changed**
- We have updated the pre-commit hooks


1.4.6 (2023-01-31)
------------------

**Added**
- We have added a new `JavascriptCode` class to encapsulate JS Code.
This will let the user set JS values for some options like `columnDefs.render` ([#154](https://github.com/mwouts/itables/issues/154)).


1.4.5 (2023-01-23)
------------------

**Fixed**
- Fixed an issue when `lengthMenu` is a 2D array ([#151](https://github.com/mwouts/itables/issues/151))


**Changed**
- We make sure that no argument passed to `show` is equal to `None` (for all tested options, passing `None` results in a datatable that never loads)
- Running the test collection will not update the CSV files used for testing anymore


1.4.4 (2023-01-15)
------------------

**Fixed**
- We have added `numpy` to the dependencies, `pytz` is an optional dependency (used in the sample dataframes only), and we do not depend on `six` anymore ([#149](https://github.com/mwouts/itables/issues/149))
The build time dependencies `pathlib` and `requests` are listed in `pyproject.toml` (since [#123](https://github.com/mwouts/itables/issues/123), `itables==1.4.0`)


1.4.3 (2023-01-14)
------------------

**Changed**
- When a table is made of only a few rows, we display just the table (not the search box, pagination control, etc)


1.4.2 (2022-12-23)
------------------

**Fixed**
- We make sure that the table content has the same number of columns as the header ([#141](https://github.com/mwouts/itables/issues/141))
- We have updated the documentation on column widths ([#145](https://github.com/mwouts/itables/issues/145))


1.4.1 (2022-12-04)
------------------

**Fixed**
- We have added `setuptools.build_meta` as the build backend in `pyproject.toml` ([#142](https://github.com/mwouts/itables/issues/142))
- We have fixed a typo in `itables.options.style`

**Changed**
- We have updated the development status of the project to _Production/Stable_


1.4.0 (2022-12-04)
------------------

**Fixed**
- We have improved the support for dark themes by using the CSS from datatables.net in version 1.13.1 ([#103](https://github.com/mwouts/itables/issues/103))
- We have fixed a compatibility issue with old versions of pandas
- We have added a test to make sure that timezones are preserved
- `requests` was added as a build dependency ([#123](https://github.com/mwouts/itables/issues/123))
- and the `flake8` pre-commit hook was fixed ([#124](https://github.com/mwouts/itables/issues/124)) - thanks
to [Anselm Hahn](https://github.com/Anselmoo) for these two contributions!
- Duplicated column and index names are supported ([#134](https://github.com/mwouts/itables/issues/134))

**Added**
- The examples in the documentation are now executed as part of the test suite to increase the coverage.
- We have added a new `caption` argument to the `show` function to make it easier to add captions on tables.

**Changed**
- We have changed the default table to `style = "table-layout:auto;width:auto;margin:auto"` to fix an issue on the width of index columns (default `style` was `width:auto` previously) ([#130](https://github.com/mwouts/itables/issues/130))
- The default classes applied to datatables are now `["display", "nowrap"]`
- We have changed the default order to `order = []` i.e. we don't sort anymore the table, even when the index is monotonic, to fix an issue in the order of categories ([#135](https://github.com/mwouts/itables/issues/135))
- We have set an explicit `maxRows = 0` and also increased `maxColumns` to `200` (instead of Pandas' default at 20).


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
