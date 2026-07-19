import re
from pathlib import Path

import pytest

from itables import to_markdown_table

try:
    from itables.sample_pandas_dfs import (
        get_dict_of_test_dfs,
    )
except ImportError:
    pytest.skip("Pandas is not available", allow_module_level=True)


@pytest.fixture(params=["int_float_str", "countries", "int_float_str_categorical"])
def df_name(request):
    return request.param


@pytest.fixture
def df(df_name):
    if df_name == "int_float_str_categorical":
        pd = pytest.importorskip("pandas")

        df = get_dict_of_test_dfs()["int_float_str"].head().copy()
        df["category"] = pd.Categorical(["low", "medium", "high", "medium", "low"])
        return df

    return get_dict_of_test_dfs()[df_name].head()


def test_to_markdown_table(df_name, df):
    ref_md_file = (
        Path(__file__).parent / "data" / "test_to_markdown_table" / f"{df_name}.md"
    )

    # connected=True makes the test deterministic regardless of the global
    # 'connected' state left behind by other tests / init_notebook_mode()
    markdown = to_markdown_table(df, connected=True)

    if not ref_md_file.exists():
        ref_md_file.parent.mkdir(parents=True, exist_ok=True)
        ref_md_file.write_text(markdown)
        assert (
            False
        ), f"Reference Markdown file created at {ref_md_file}. Please verify it and run the test again."

    # ref_md_file has a trailing newline added by the end-of-file-fixer
    # pre-commit hook, which to_markdown_table()'s return value doesn't have
    # (it's meant to be printed, not written to a file, cf. show()).
    expected_markdown = ref_md_file.read_text().rstrip("\n")
    assert (
        markdown == expected_markdown
    ), f"Generated Markdown does not match reference for {df_name}."


def _row_count(markdown: str) -> int:
    # every table row starts with "| ", minus the header and separator rows
    return sum(1 for line in markdown.splitlines() if line.startswith("| ")) - 2


def test_default_pagination_shows_ten_rows():
    df = get_dict_of_test_dfs()["int_float_str"]
    assert len(df) == 100

    markdown = to_markdown_table(df)
    assert _row_count(markdown) == 10
    assert "90 more rows not shown" in markdown


def test_page_length_option_is_respected():
    df = get_dict_of_test_dfs()["int_float_str"]

    assert _row_count(to_markdown_table(df, pageLength=3)) == 3
    assert _row_count(to_markdown_table(df, lengthMenu=[5, 10, 25])) == 5


def test_paging_false_shows_all_rows():
    df = get_dict_of_test_dfs()["int_float_str"].head(20)

    markdown = to_markdown_table(df, paging=False)
    assert _row_count(markdown) == 20
    assert "not shown" not in markdown


def test_downsampling_note_is_shown():
    df = get_dict_of_test_dfs()["int_float_str"]
    assert len(df) == 100

    # the note counts rows missing relative to the original dataframe, not
    # just the ones dropped by pagination on top of downsampling (#575)
    markdown = to_markdown_table(df, maxRows=30, paging=False)
    assert _row_count(markdown) == 30
    assert "70 more rows not shown" in markdown


def test_downsampled_columns_note_is_shown():
    pd = pytest.importorskip("pandas")
    df = pd.DataFrame({f"c{i}": range(5) for i in range(20)})

    markdown = to_markdown_table(df, maxColumns=5)
    assert "15 more columns not shown" in markdown


def test_show_df_type_note_is_shown():
    df = get_dict_of_test_dfs()["int_float_str"].head()
    markdown = to_markdown_table(df, show_df_type=True)
    assert "pandas.DataFrame" in markdown


def test_none_dataframe():
    assert "no static preview" in to_markdown_table(None)


def _cells(line: str) -> list:
    # "| a | bb |" -> ["a", "bb"] (columns are padded for alignment;
    # an escaped "\|" inside a cell must not be treated as a separator)
    return [
        cell.strip().replace("\\|", "|")
        for cell in re.split(r"(?<!\\)\|", line.strip().strip("|"))
    ]


def test_special_characters_are_escaped():
    pd = pytest.importorskip("pandas")
    df = pd.DataFrame({"a|b": ["a value", "pipe | here"]})
    markdown = to_markdown_table(df)

    # the raw pipe in the column name and in a cell must not have
    # introduced extra table cells/rows (there is a single, un-named
    # column, so every row is "| <cell> |")
    table_lines = [line for line in markdown.splitlines() if line.startswith("| ")]
    header, separator, *body_rows = table_lines
    assert _cells(header) == ["a|b"]
    assert set(_cells(separator)[0]) == {"-"}
    assert [_cells(row) for row in body_rows] == [["a value"], ["pipe | here"]]


def test_embedded_newlines_do_not_break_the_table():
    pd = pytest.importorskip("pandas")
    df = pd.DataFrame({"a": ["line1\nline2"]})
    markdown = to_markdown_table(df)

    # whether pandas' own formatting or _markdown_escape_cell neutralizes
    # the embedded newline, it must not have introduced an extra table row
    table_lines = [line for line in markdown.splitlines() if line.startswith("| ")]
    assert len(table_lines) == 3  # header, separator, one data row


def test_styler_falls_back_to_its_underlying_data():
    # A Styler's formatting/highlighting is arbitrary HTML that can't be
    # expressed in Markdown, but its underlying data can still be shown as a
    # plain table - unlike the interactive table, this doesn't require
    # allow_html=True, since we never touch the Styler's HTML
    pd = pytest.importorskip("pandas")
    pytest.importorskip("jinja2")

    styler = pd.DataFrame({"x": [1, 2]}).style.highlight_max(color="yellow")
    markdown = to_markdown_table(styler)
    assert "no static preview" not in markdown
    assert _cells(markdown.splitlines()[2]) == ["1"]
    assert to_markdown_table(styler, allow_html=True) == markdown
