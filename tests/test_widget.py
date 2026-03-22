import pytest

import itables.options as opt
import itables.sample_dfs

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

    itable = ITable(df, format_floats_in_python=False)
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


def test_update_clears_stale_column_defs():
    """Updating a widget to a dataframe with a different column structure
    should not leave stale auto-generated columnDefs or keys_to_be_evaluated
    in _dt_args (regression test for
    https://github.com/mwouts/itables/issues/526).
    """
    pd = pytest.importorskip("pandas")

    from itables.widget import ITable

    dict_of_test_dfs = itables.sample_dfs.get_dict_of_test_dfs()

    # Step 1: empty table
    table = ITable(dict_of_test_dfs["empty"])
    assert "columnDefs" not in table._dt_args
    assert "keys_to_be_evaluated" not in table._dt_args

    # Step 2: update with a dataframe that contains a float column, which
    # causes auto-generated columnDefs / keys_to_be_evaluated to be added
    data_with_float = pd.DataFrame(
        {
            "col1": ["row1", "row2"],
            "col2": ["row1", "row2"],
            "col3": [1, 2],
            "col4": [1.0, 2.0],
            "col5": ["a", "b"],
            "col6": ["c", "d"],
            "col7": ["e", "f"],
        }
    )
    table.update(data_with_float)
    assert "columnDefs" in table._dt_args
    assert "keys_to_be_evaluated" in table._dt_args

    # Step 3: update back to an empty table – stale keys must be removed so
    # that DataTables does not raise "Requested unknown parameter" warnings
    table.update(dict_of_test_dfs["empty"])
    assert "columnDefs" not in table._dt_args, table._dt_args.get("columnDefs")
    assert "keys_to_be_evaluated" not in table._dt_args, table._dt_args.get(
        "keys_to_be_evaluated"
    )
