import itables.options as opt
from itables.widget import ITable


def test_create_widget_with_no_df():
    itable = ITable()
    assert itable._df is None
    assert itable.caption == ""
    assert itable.classes == opt.classes
    assert itable.style == opt.style
    assert itable.selected_rows == []
    assert itable._dt_args == {
        "order": [],
        "layout": {k: None for k in opt.layout},
    }


def test_create_widget_with_df(df):
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
        "order": [],
    }
