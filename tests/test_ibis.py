import pytest

from itables import to_html_datatable
from itables.sample_dfs import get_dict_of_test_dfs

try:
    import ibis  # noqa
except ImportError as e:
    pytest.skip(str(e), allow_module_level=True)

# TODO Remove this (and find out how to evaluate count)
ibis.options.interactive = True


@pytest.mark.parametrize(
    "name,df",
    [(name, df) for name, df in get_dict_of_test_dfs(type="ibis_memtable").items()],
)
def test_show_ibis_memtable(name, df, use_to_html):
    to_html_datatable(df, use_to_html)


@pytest.mark.parametrize(
    "name,df",
    [(name, df) for name, df in get_dict_of_test_dfs(type="ibis_connect").items()],
)
def test_show_ibis_connect(name, df, use_to_html):
    to_html_datatable(df, use_to_html)
