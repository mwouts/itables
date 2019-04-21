import re
import pytest
from slimit.parser import Parser
from itables.javascript import _datatables_repr_
from itables.sample import sample_dfs, sample_series


@pytest.fixture()
def parser():
    return Parser()


def test_incorrect_js_raises(parser):
    incorrect_script = """x = (1 + 5;"""
    with pytest.raises(SyntaxError):
        parser.parse(incorrect_script)


@pytest.mark.parametrize('df', sample_dfs())
def test_sample_tables(df, parser):
    html = _datatables_repr_(df)
    js_re = re.compile('.*<script type="text/javascript">(.*)</script>', flags=re.M | re.DOTALL)
    script = js_re.match(html).groups()[0]
    parser.parse(script)


@pytest.mark.parametrize('x', sample_series())
def test_sample_series(x, parser):
    html = _datatables_repr_(x)
    js_re = re.compile('.*<script type="text/javascript">(.*)</script>', flags=re.M | re.DOTALL)
    script = js_re.match(html).groups()[0]
    parser.parse(script)
