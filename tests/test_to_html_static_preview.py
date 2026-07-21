import pytest

from itables import to_html_static_preview

try:
    from itables.sample_pandas_dfs import get_dict_of_test_dfs
except ImportError:
    pytest.skip("Pandas is not available", allow_module_level=True)


def _row_count(html: str) -> int:
    # every data row is written as "<tr><td ...", cf. _simple_html_table_from_dt_args()
    body = html.split("<tbody>", 1)[1].split("</tbody>", 1)[0]
    return body.count("<tr><td")


def test_default_pagination_shows_ten_rows():
    df = get_dict_of_test_dfs()["int_float_str"]
    assert len(df) == 100

    html = to_html_static_preview(df)
    assert _row_count(html) == 10
    assert "(90 more rows not shown)" in html


def test_page_length_option_is_respected():
    df = get_dict_of_test_dfs()["int_float_str"]

    assert _row_count(to_html_static_preview(df, pageLength=3)) == 3
    assert _row_count(to_html_static_preview(df, lengthMenu=[5, 10, 25])) == 5


def test_paging_false_shows_all_rows():
    df = get_dict_of_test_dfs()["int_float_str"].head(20)

    html = to_html_static_preview(df, paging=False)
    assert _row_count(html) == 20
    assert "not shown" not in html


def test_downsampling_note_is_shown_in_tfoot():
    df = get_dict_of_test_dfs()["int_float_str"]
    assert len(df) == 100

    # the note counts rows missing relative to the original dataframe, not
    # just the ones dropped by pagination on top of downsampling (#575)
    html = to_html_static_preview(df, maxRows=30, paging=False)
    assert _row_count(html) == 30
    assert "<tfoot>" in html
    assert "(70 more rows not shown)" in html.split("<tfoot>", 1)[1]


def test_downsampled_columns_note_is_shown():
    pd = pytest.importorskip("pandas")
    df = pd.DataFrame({f"c{i}": range(5) for i in range(20)})

    html = to_html_static_preview(df, maxColumns=5)
    assert "(15 more columns not shown)" in html.split("<tfoot>", 1)[1]


def test_show_df_type_note_is_shown_when_nothing_is_downsampled():
    pd = pytest.importorskip("pandas")
    df = pd.DataFrame({"x": [1]})

    html = to_html_static_preview(df, show_df_type=True)
    assert "pandas.DataFrame" in html.split("<tfoot>", 1)[1]


def test_hidden_rows_note_uses_full_column_span():
    pd = pytest.importorskip("pandas")
    df = pd.DataFrame({"a": range(20), "b": range(20), "c": range(20)})

    html = to_html_static_preview(df)
    tfoot = html.split("<tfoot>", 1)[1].split("</tfoot>", 1)[0]
    assert 'colspan="3"' in tfoot
    assert tfoot.endswith("(10 more rows not shown)</td></tr>")


def test_static_preview_marker_is_in_the_header_not_the_footer():
    pd = pytest.importorskip("pandas")
    df = pd.DataFrame({"x": range(20)})

    html = to_html_static_preview(df)
    thead = html.split("<thead>", 1)[1].split("</thead>", 1)[0]
    tfoot = html.split("<tfoot>", 1)[1].split("</tfoot>", 1)[0]
    assert "static preview" in thead
    assert "static preview" not in tfoot
    assert "10 more rows not shown" in tfoot


def test_no_footer_without_any_notes():
    pd = pytest.importorskip("pandas")
    df = pd.DataFrame({"x": [1]})

    html = to_html_static_preview(df)
    assert "<tfoot>" not in html


def test_static_preview_marker_mentions_the_version():
    pd = pytest.importorskip("pandas")
    from itables.version import __version__

    df = pd.DataFrame({"x": [1]})
    html = to_html_static_preview(df)
    thead = html.split("<thead>", 1)[1].split("</thead>", 1)[0]
    # a small, linked "info" marker with a tooltip, rather than a sentence
    # of always-visible text. No "trust this notebook" hint here: this
    # standalone static preview isn't paired with an interactive table and
    # a swap script - see test_to_html_datatable.py for that case.
    assert (
        "<sup><a href=https://itables.org/fallbacks/static_preview.html "
        f'title="ITables v{__version__} static preview">ⓘ</a></sup>'
    ) in thead


def _tfoot(html: str) -> str:
    return html.split("<tfoot>", 1)[1].split("</tfoot>", 1)[0]


def _thead(html: str) -> str:
    return html.split("<thead>", 1)[1].split("</thead>", 1)[0]


def test_caption_is_rendered_as_a_row_not_a_caption_tag():
    # GitHub's notebook sanitizer strips <caption> tags (the text then
    # foster-parents out of the table, above it), so we use a table row
    # instead - see _caption_as_row() and #575
    pd = pytest.importorskip("pandas")
    df = pd.DataFrame({"x": [1]})

    html = to_html_static_preview(df, caption="My caption")
    assert "<caption" not in html
    assert "My caption" in html


def test_no_caption_row_without_an_explicit_caption():
    pd = pytest.importorskip("pandas")
    df = pd.DataFrame({"x": [1]})

    html = to_html_static_preview(df)
    assert "<caption" not in html
    assert "<tfoot>" not in html


def test_caption_is_placed_below_the_table_by_default():
    # like in the interactive table, the caption goes below the table - here
    # in a <tfoot> row, so it survives GitHub's sanitizer (#575)
    pd = pytest.importorskip("pandas")
    df = pd.DataFrame({"x": [1]})

    html = to_html_static_preview(df, caption="My caption")
    assert "My caption" in _tfoot(html)
    assert "My caption" not in _thead(html)


def test_caption_and_rows_not_shown_note_share_one_row():
    # the note joins the caption's own row, in parentheses, on a new line -
    # rather than getting its own (bordered) row below
    pd = pytest.importorskip("pandas")
    df = pd.DataFrame({"x": range(20)})

    html = to_html_static_preview(df, caption="My caption")
    tfoot = _tfoot(html)
    assert tfoot.count("<tr>") == 1
    assert "My caption<br>(10 more rows not shown)" in tfoot


def test_rows_not_shown_note_keeps_its_own_row_without_a_caption():
    pd = pytest.importorskip("pandas")
    df = pd.DataFrame({"x": range(20)})

    tfoot = _tfoot(to_html_static_preview(df))
    assert "(10 more rows not shown)" in tfoot
    assert "border:none" in tfoot


def test_caption_side_top_places_the_caption_above_the_header():
    pd = pytest.importorskip("pandas")
    df = pd.DataFrame({"x": [1]})

    html = to_html_static_preview(
        df, caption="My caption", style="width:auto;caption-side:top"
    )
    thead = _thead(html)
    assert "My caption" in thead
    # above the header row, i.e. before the first <th>
    assert thead.index("My caption") < thead.index("<th")
    assert "<tfoot>" not in html


def test_none_dataframe():
    assert to_html_static_preview(None) == ""


def test_styler_requires_allow_html():
    pd = pytest.importorskip("pandas")
    pytest.importorskip("jinja2")

    styler = pd.DataFrame({"x": [1, 2]}).style
    with pytest.raises(ValueError, match="allow_html=True"):
        to_html_static_preview(styler)


def test_styler_with_allow_html_reuses_table_html():
    pd = pytest.importorskip("pandas")
    pytest.importorskip("jinja2")

    styler = pd.DataFrame({"x": [1, 2]}).style
    html = to_html_static_preview(styler, allow_html=True)
    assert "static preview" in html.split("<thead>", 1)[1].split("</thead>", 1)[0]
    assert "<td" in html and ">1<" in html and ">2<" in html


def test_styler_own_caption_is_rescued_into_a_row():
    # a caption set on the Styler itself (set_caption) would also be stripped
    # by GitHub, so it too is turned into a <tfoot> row (#575)
    pd = pytest.importorskip("pandas")
    pytest.importorskip("jinja2")

    styler = pd.DataFrame({"x": [1, 2]}).style.set_caption("Styler caption")
    html = to_html_static_preview(styler, allow_html=True)
    assert "<caption" not in html
    assert "Styler caption" in _tfoot(html)
