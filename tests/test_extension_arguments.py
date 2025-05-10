import pytest

from itables.javascript import get_itables_extension_arguments


def test_get_itables_extension_arguments(df):
    try:
        dt_args, other_args = get_itables_extension_arguments(df)
    except NotImplementedError as e:
        pytest.skip(str(e))

    assert set(dt_args) <= {
        "table_html",
        "data_json",
        "column_filters",
        "layout",
        "order",
        "text_in_header_can_be_selected",
        "filtered_row_count",
        "downsampling_warning",
    }, set(dt_args)
    assert isinstance(dt_args["data_json"], str)  # type: ignore
    assert isinstance(dt_args["table_html"], str)  # type: ignore

    assert set(other_args) <= {
        "classes",
        "style",
        "caption",
        "selected_rows",
    }, set(dt_args)
    assert isinstance(other_args["classes"], str)
    assert isinstance(other_args["style"], str)
    assert other_args["caption"] is None
