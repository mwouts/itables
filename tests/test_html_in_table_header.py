import pandas as pd

from itables import to_html_datatable


def test_html_in_table_header(df=pd.DataFrame({"<b>B</b>": [1]})):
    html = to_html_datatable(df)
    print(html)
    assert "<b>B</b>" in html
