import pytest

from itables import to_html_datatable
from itables.sample_dfs import get_dict_of_test_dfs, get_dict_of_test_series

try:
    import polars  # noqa
except ImportError as e:
    pytest.skip(str(e), allow_module_level=True)


@pytest.mark.parametrize(
    "name,x", [(name, x) for name, x in get_dict_of_test_series(polars=True).items()]
)
def test_show_polars_series(name, x):
    to_html_datatable(x)


@pytest.mark.parametrize(
    "name,df", [(name, df) for name, df in get_dict_of_test_dfs(polars=True).items()]
)
def test_show_polars_df(name, df):
    to_html_datatable(df)
