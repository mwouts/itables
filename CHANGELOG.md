0.3.0 (2020-12-11)
==================

Fixed
-------
- `itables` now has an explicit `init_notebook_mode` function, which inserts the datatables.net library in the notebook. Use `init_notebook_mode(all_interactive=True)` to display all the pandas object as interactive tables. This fixes (#6) and (#17).

0.2.2 (2020-10-01)
==================

Fixed
-----
- Pandas' `display.max_columns` can be `None`, by Arthur Deygin (#14)


0.2.1 (2019-11-21)
==================

Added
-----
- Animated screenshot in README

Fixed
-----
- Add IPython to setup.py install_requires, by Jon Shao (#9)


0.2.0 (2019-11-20)
==================

Added
-----
- Large tables are downsampled (#2)

Changed
-------
- Javascript code moved to Javascript files

Fixed
-----
- Tables with many columns are now well rendered (#5)


0.1.0 (2019-04-23)
==================

Initial release
