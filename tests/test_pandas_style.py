import json

import pytest

from itables import to_html_datatable
from itables.javascript import get_itable_arguments

pytest.importorskip("jinja2")

try:
    import pandas as pd
except ImportError:
    pytest.skip("Pandas is not available", allow_module_level=True)


def test_buttons_are_shown_on_pd_style_objects():
    df = pd.DataFrame({"A": ["a"]}).style
    html = to_html_datatable(
        df,
        buttons=["pageLength", "copyHtml5", "csvHtml5", "excelHtml5"],
        allow_html=True,
    )

    # Extract the dt_args passed to datatables
    dt_args = ""
    for line in html.splitlines():
        line = line.strip()
        if line.startswith("let dt_args"):
            dt_args = line.split("=", 1)[1]
            break

    assert dt_args.endswith(";"), dt_args
    dt_args = dt_args[:-1]
    dt_args = json.loads(dt_args)

    print(dt_args)
    assert "dom" not in dt_args
    assert "buttons" in dt_args
    assert "buttons" in dt_args["layout"].values()


def test_non_trivial_index_of_styler_objects_are_included():
    """
    When a Pandas Styler index is non trivial, it should appear
    in the ITable output, see issue #393
    """
    df = pd.DataFrame({"A": [1]}, index=pd.Index([0], name="index"))
    dt_args = get_itable_arguments(df.style, table_id="T_id", allow_html=True)
    assert "table_html" in dt_args
    table_html = dt_args["table_html"]
    assert "index" in table_html, table_html


@pytest.mark.parametrize("showIndex", [True, "auto"])
def test_trivial_indexes_of_styler_objects_are_not_included(showIndex):
    """
    When a Pandas Styler index is trivial, it should appear
    in the ITable output only if showIndex is True
    """
    df = pd.DataFrame({"A": [1]})
    dt_args = get_itable_arguments(
        df.style, table_id="T_id", allow_html=True, showIndex=showIndex
    )
    assert "table_html" in dt_args
    table_html = dt_args["table_html"]
    assert ('class="blank level0"' in table_html) == (showIndex is True), table_html
