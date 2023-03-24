from itables.javascript import _df_fits_in_one_page, to_html_datatable


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
