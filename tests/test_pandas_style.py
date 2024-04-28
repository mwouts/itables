import json

import pandas as pd
import pytest

from itables import to_html_datatable

pytest.importorskip("jinja2")


@pytest.mark.skipif(
    pd.__version__.startswith("0."),
    reason="AttributeError: 'Styler' object has no attribute 'to_html'",
)
def test_buttons_are_shown_on_pd_style_objects():
    df = pd.DataFrame({"A": ["a"]}).style
    html = to_html_datatable(
        df, buttons=["pageLength", "copyHtml5", "csvHtml5", "excelHtml5"]
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
