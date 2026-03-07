from pathlib import Path
from unittest.mock import patch

import pytest

from itables import to_html_datatable

try:
    from itables.sample_pandas_dfs import (
        get_dict_of_test_dfs,
    )
except ImportError:
    pytest.skip("Pandas is not available", allow_module_level=True)


@pytest.fixture(params=["int_float_str", "countries"])
def df_name(request):
    return request.param


@pytest.fixture
def df(df_name):
    return get_dict_of_test_dfs()[df_name].head()


def test_to_html_datatable(df_name, df):
    ref_html_file = (
        Path(__file__).parent / "data" / "test_to_html_datatable" / f"{df_name}.html"
    )

    # Mock version numbers to make test version-independent
    with (
        patch("itables.javascript.itables_version", "{itables_version}"),
        patch(
            "itables.options.dt_url",
            "https://www.unpkg.com/dt_for_itables@{dt_for_itables_version}/dt_bundle.js",
        ),
    ):
        html = to_html_datatable(
            df, table_id="table_id", display_logo_when_loading=False, connected=True
        )

    if not ref_html_file.exists():
        ref_html_file.parent.mkdir(parents=True, exist_ok=True)
        ref_html_file.write_text(html)
        assert (
            False
        ), f"Reference HTML file created at {ref_html_file}. Please verify it and run the test again."

    expected_html = ref_html_file.read_text()
    assert (
        html == expected_html
    ), f"Generated HTML does not match reference for {df_name}."
