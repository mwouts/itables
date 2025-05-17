import pytest

import itables.options as opt

pytest.importorskip("anywidget")


def test_create_widget_with_no_df():
    from itables.widget import ITable

    itable = ITable()
    assert itable._df is None
    assert itable.caption == ""
    assert itable.classes == opt.classes
    assert itable.style == opt.style
    assert itable.selected_rows == []
    assert itable._dt_args == {
        "text_in_header_can_be_selected": True,
        "order": [],
        "layout": {k: None for k in opt.layout},
    }


def test_create_widget_with_df(df):
    from itables.widget import ITable

    itable = ITable(df)
    assert itable.df is df
    assert itable.caption == ""
    assert itable.classes == opt.classes
    assert itable.style == opt.style
    assert itable.selected_rows == []
    selected_dt_args = {
        k: v
        for k, v in itable._dt_args.items()
        if k
        not in [
            "data_json",
            "table_html",
            "filtered_row_count",
            "downsampling_warning",
            "layout",
        ]
    }
    assert selected_dt_args == {
        "text_in_header_can_be_selected": True,
        "order": [],
    }
