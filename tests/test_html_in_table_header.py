import pytest

try:
    import pandas as pd
except ImportError:
    pd = None
    pytest.skip("Pandas is not available", allow_module_level=True)

from itables import to_html_datatable


@pytest.mark.parametrize("allow_html", [True, False])
def test_html_in_table_header(allow_html, df=pd.DataFrame({"<b>B</b>": [1]})):
    html = to_html_datatable(df, allow_html=allow_html)
    print(html)
    assert ("<b>B</b>" in html) == allow_html
