# 2.5.0 (2026-02-01)

- We have updated datatables and its extensions to `datatables.net-dt==2.3.7`


# 2.4.0 (2025-08-23)

- We have added the ColumnControl extension of DataTables to the `dt_for_itables` package ([#403](https://github.com/mwouts/itables/issues/403))


# 2.3.3 (2025-06-10)

- We have made sure that the ordering icons on empty headers do not reappear when ordering a column
- Wrapping Javascript functions definitions within parentheses before evaluating is now done on the Javascript side
- The CSS imports have been moved to the `.css` files, and we extend the `:root` styles to `:host`


# 2.3.2 (2025-05-17)

- We have fixed an issue with `selected_rows` when `filtered_row_count` was not explicitly set.

# 2.3.1 (2025-05-17)

- We have improved the implementation of `text_in_header_can_be_selected`.
- The indirect evaluation of `JavascriptCode` and `JavascriptFunction` will not proceed when prototype pollution attempts are detected.

# 2.3.0 (2025-05-11)

- This version uses `datatables.net-dt=2.3.0`. The extensions have been updated, too.
- We have added a new class `ITable` that processes some of the arguments on the Javascript side.
- We use an indirect eval to parse the `JavascriptCode` and `JavascriptFunction` passed from Python.
- The table data is now passed as JSON through `data_json`, with support for BigInts and non finite float values.

# 2.2.0 (2025-03-15)

- We have upgraded `datatables.net-dt==2.2.2` and `datatables.net-select-dt==3.0.0`

# 2.0.13 (2024-09-22)

- We have added two functions `set_selected_rows` and `get_selected_rows` to set and retrieve selected rows

# 2.0.12 (2024-09-08)

- We have added the datetime extension for DataTables ([#288](https://github.com/mwouts/itables/issues/288))

# 2.0.11 (2024-06-19)

**Added**
- The default CSS contains has `overflow:auto` on `.dt-layout-table>div`. This improves the horizontal scrolling in Jupyter, and discards the need for `scrollX` in Streamlit ([#282](https://github.com/mwouts/itables/pull/282))


# 2.0.10 (2024-06-08)

**Added**
- The default css for `dt-container` is `{max-width:100%;}`
- We have included the `colvis` button in the package

**Changed**
- Updated `datatables.net-dt==2.0.8` and `datatables.net-select-dt==2.0.3`


# 2.0.7 (2024-05-26)

**Added**
- Added a default export and typings

**Changed**
- Updated `datatables.net-dt==2.0.7` and `datatables.net-select-dt==2.0.2`
