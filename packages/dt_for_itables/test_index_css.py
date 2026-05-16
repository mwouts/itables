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
