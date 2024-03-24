import json
from pathlib import Path

import pytest
import requests

from itables.javascript import (
    UNPKG_DT_BUNDLE_CSS,
    UNPKG_DT_BUNDLE_URL,
    _df_fits_in_one_page,
    _tfoot_from_thead,
    check_table_id,
    replace_value,
    to_html_datatable,
)


def test_replace_value(
    template="line1\nline2\nline3\n", pattern="line2", value="new line2"
):
    assert replace_value(template, pattern, value) == "line1\nnew line2\nline3\n"


def test_replace_value_not_found(
    template="line1\nline2\nline3\n", pattern="line4", value="new line4"
):
    with pytest.raises(ValueError, match="not found"):
        assert replace_value(template, pattern, value)


def test_replace_value_multiple(
    template="line1\nline2\nline2\n", pattern="line2", value="new line2"
):
    with pytest.raises(ValueError, match="found multiple times"):
        assert replace_value(template, pattern, value)


def test_warn_on_unexpected_types_not_in_html(df):
    html = to_html_datatable(df)
    assert "warn_on_unexpected_types" not in html


def test_df_fits_in_one_page(df, lengthMenu):
    kwargs = dict(lengthMenu=lengthMenu)
    kwargs = {key: value for key, value in kwargs.items() if value is not None}

    if lengthMenu is None:
        assert _df_fits_in_one_page(df, kwargs) == (len(df) <= 10)
        return

    min_rows = lengthMenu[0]
    if isinstance(min_rows, list):
        min_rows = min_rows[0]

    assert _df_fits_in_one_page(df, kwargs) == (len(df) <= min_rows)


def test_tfoot_from_thead(
    thead="""
    <tr style="text-align: right;">
      <th></th>
      <th>region</th>
      <th>country</th>
      <th>capital</th>
      <th>longitude</th>
      <th>latitude</th>
      <th>flag</th>
    </tr>
    <tr>
      <th>code</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
""",
    expected_tfoot="""
    <tr>
      <th>code</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
    <tr style="text-align: right;">
      <th></th>
      <th>region</th>
      <th>country</th>
      <th>capital</th>
      <th>longitude</th>
      <th>latitude</th>
      <th>flag</th>
    </tr>
""",
):
    assert _tfoot_from_thead(thead) == expected_tfoot


def test_check_table_id():
    with pytest.raises(ValueError, match="cannot start with a number"):
        check_table_id("0_invalid_id")
    check_table_id("valid_id")
    check_table_id("valid_id-2")


@pytest.mark.parametrize("url", [UNPKG_DT_BUNDLE_URL, UNPKG_DT_BUNDLE_CSS])
def test_unpkg_links(url):
    response = requests.get(url)
    assert response.ok, url


def test_unpkg_urls_are_up_to_date():
    with open(Path(__file__).parent / "../packages/dt_for_itables/package.json") as fp:
        dt_for_itables = json.load(fp)
    bundle_version = dt_for_itables["version"]
    assert (
        UNPKG_DT_BUNDLE_URL
        == f"https://www.unpkg.com/dt_for_itables@{bundle_version}/dt_bundle.js"
    )
    assert (
        UNPKG_DT_BUNDLE_CSS
        == f"https://www.unpkg.com/dt_for_itables@{bundle_version}/dt_bundle.css"
    )
