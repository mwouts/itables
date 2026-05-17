from pathlib import Path


def test_order_icons_stay_on_the_right_in_headers_and_footers():
    css = (Path(__file__).parent / "src/index.css").read_text()
    expected_wrapper_rule = """table.dataTable thead > tr > th div.dt-column-header,
table.dataTable thead > tr > td div.dt-column-header,
table.dataTable tfoot > tr > th div.dt-column-footer,
table.dataTable tfoot > tr > td div.dt-column-footer {
    flex-direction: row !important;
}"""
    assert expected_wrapper_rule in css


def test_column_control_search_row_does_not_wrap():
    css = (Path(__file__).parent / "src/index.css").read_text()
    expected_rule = """div.dtcc-dropdown div.dtcc-search > div {
    flex-wrap: nowrap;
}"""
    assert expected_rule in css
