import pytest

from itables import to_html_static_preview

try:
    from itables.sample_pandas_dfs import get_dict_of_test_dfs
except ImportError:
    pytest.skip("Pandas is not available", allow_module_level=True)


def _row_count(html: str) -> int:
    # every data row is written as "<tr><td>...", cf. _simple_html_table_from_dt_args()
    return html.count("<tr><td>")


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
    assert '<tfoot><tr><td colspan="3">10 more rows not shown</td></tr></tfoot>' in html


def test_caption_combines_original_caption_with_message():
    pd = pytest.importorskip("pandas")
    df = pd.DataFrame({"x": [1]})

    html = to_html_static_preview(df, caption="My caption")
    caption = html.split("<caption>", 1)[1].split("</caption>", 1)[0]
    assert caption.startswith("My caption<br>")
    assert "ITables can't run JavaScript in this context" in caption


def test_caption_is_just_the_message_without_an_explicit_caption():
    pd = pytest.importorskip("pandas")
    df = pd.DataFrame({"x": [1]})

    html = to_html_static_preview(df)
    caption = html.split("<caption>", 1)[1].split("</caption>", 1)[0]
    assert caption == (
        "ITables can't run JavaScript in this context - defaulting to a "
        "<a href=https://mwouts.github.io/itables/troubleshooting.html"
        "#static-preview-instead-of-the-interactive-table>static preview</a>"
    )


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
    assert "<caption>" in html
    assert "<td" in html and ">1<" in html and ">2<" in html
