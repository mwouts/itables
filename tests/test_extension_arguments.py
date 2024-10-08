import pandas as pd
import pytest

from itables import JavascriptCode
from itables.javascript import get_itables_extension_arguments, pd_style


def test_get_itables_extension_arguments(df):
    try:
        dt_args, other_args = get_itables_extension_arguments(df)
    except NotImplementedError as e:
        pytest.skip(str(e))

    assert set(dt_args) <= {
        "data",
        "columns",
        "layout",
        "order",
    }, set(dt_args)
    assert isinstance(dt_args["data"], list)
    assert isinstance(dt_args["columns"], list)

    assert set(other_args) <= {
        "classes",
        "style",
        "caption",
        "downsampling_warning",
        "selected_rows",
        "filtered_row_count",
    }, set(dt_args)
    assert isinstance(other_args["classes"], str)
    assert isinstance(other_args["style"], str)
    assert other_args["caption"] is None


def test_no_use_to_html():
    with pytest.raises(
        TypeError,
        match="In the context of the itable widget or streamlit extension, these options are not available",
    ):
        get_itables_extension_arguments(pd.DataFrame({"a": [0]}), use_to_html=True)


def test_no_javascript_code():
    with pytest.raises(
        TypeError, match="Javascript code can't be passed to the extension"
    ):
        get_itables_extension_arguments(
            pd.DataFrame({"a": [0]}),
            columnDefs=[
                {
                    "targets": "_all",
                    "render": JavascriptCode(
                        "$.fn.dataTable.render.number(',', '.', 3, '$')"
                    ),
                }
            ],
        )


def test_no_style_object():
    if pd_style is None:
        pytest.skip("Pandas Style is not available")
    with pytest.raises(
        NotImplementedError,
        match="Pandas style objects can't be used with the extension",
    ):
        get_itables_extension_arguments(pd.DataFrame({"a": [0]}).style)
