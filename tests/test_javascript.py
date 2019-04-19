import re
import pytest
from slimit.parser import Parser
from itables.javascript import datatables
from .sample_tables import sample_tables, table_with_complex_header, sample_series


@pytest.fixture()
def parser():
    return Parser()


def test_incorrect_js_raises(parser):
    incorrect_script = """x = (1 + 5;"""
    with pytest.raises(SyntaxError):
        parser.parse(incorrect_script)


@pytest.mark.parametrize('df', sample_tables() + [table_with_complex_header()])
def test_sample_tables(df, parser):
    script = datatables(df)
    multiline_js_string = re.compile('`(.*)`', flags=re.M | re.DOTALL)
    script = re.sub(multiline_js_string, '', script)
    parser.parse(script)


@pytest.mark.parametrize('x', sample_series())
def test_sample_series(x, parser):
    script = datatables(x)
    multiline_js_string = re.compile('`(.*)`', flags=re.M | re.DOTALL)
    script = re.sub(multiline_js_string, '', script)
    parser.parse(script)
