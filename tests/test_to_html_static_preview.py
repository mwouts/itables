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
    assert "90 more rows not shown" in html


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
    assert "70 more rows not shown" in html.split("<tfoot>", 1)[1]


def test_downsampled_columns_note_is_shown():
    pd = pytest.importorskip("pandas")
    df = pd.DataFrame({f"c{i}": range(5) for i in range(20)})

    html = to_html_static_preview(df, maxColumns=5)
    assert "15 more columns not shown" in html.split("<tfoot>", 1)[1]


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
    assert tfoot.endswith("10 more rows not shown</td></tr>")


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
    # of always-visible text
    assert (
        "<sup><a href=https://mwouts.github.io/itables/fallbacks/static_preview.html "
        f'title="ITables v{__version__} static preview">ⓘ</a></sup>'
    ) in thead


def test_caption_is_just_the_original_caption():
    pd = pytest.importorskip("pandas")
    df = pd.DataFrame({"x": [1]})

    html = to_html_static_preview(df, caption="My caption")
    caption = html.split("<caption>", 1)[1].split("</caption>", 1)[0]
    assert caption == "My caption"


def test_no_caption_tag_without_an_explicit_caption():
    pd = pytest.importorskip("pandas")
    df = pd.DataFrame({"x": [1]})

    html = to_html_static_preview(df)
    assert "<caption>" not in html


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
