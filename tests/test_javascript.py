from itables.javascript import (
    _set_dom_equals_t_if_df_fits_in_one_page,
    to_html_datatable,
)


def test_warn_on_unexpected_types_not_in_html(df):
    html = to_html_datatable(df)
    assert "warn_on_unexpected_types" not in html


def test_set_dom_equals_t_if_df_fits_in_one_page(df, dom, lengthMenu):
    kwargs = dict(lengthMenu=lengthMenu, dom=dom)
    kwargs = {key: value for key, value in kwargs.items() if value is not None}
    _set_dom_equals_t_if_df_fits_in_one_page(df, kwargs)

    if dom is not None:
        assert kwargs["dom"] == dom
        return

    if lengthMenu is None:
        if len(df) <= 10:
            assert kwargs["dom"] == "t"
            return

        assert "dom" not in kwargs
        return

    min_rows = lengthMenu[0]
    if isinstance(min_rows, list):
        min_rows = min_rows[0]

    if len(df) <= min_rows:
        assert kwargs["dom"] == "t"
        return

    assert "dom" not in kwargs
    return
