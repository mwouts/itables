import pytest

from itables.javascript import _df_fits_in_one_page, replace_value, to_html_datatable


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


def test_warn_on_int_to_str_conversion_not_in_html(df):
    html = to_html_datatable(df)
    assert "warn_on_int_to_str_conversion" not in html


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
