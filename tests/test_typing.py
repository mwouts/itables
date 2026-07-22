import re
import warnings

import pytest

import itables

if not itables.typing.is_typeguard_available():
    pytestmark = pytest.mark.skip(reason="Typeguard is not available")


@pytest.fixture
def df():
    return itables.sample_dfs.get_countries(html=False)


def test_warns_on_incorrect_option(df):
    with pytest.warns(
        SyntaxWarning,
        match="These arguments are not documented in ITableOptions: .*'lengthMenuWithTypo'",
    ):
        itables.to_html_datatable(df, lengthMenuWithTypo=[2, 5, 10])  # type: ignore


def test_warns_on_incorrect_type(df):
    with pytest.warns(SyntaxWarning, match=re.escape("does not match")):
        itables.to_html_datatable(df, lengthMenu=[2.2])  # type: ignore


"""The column definitions wrapped in an extra tuple, e.g. because of a stray
comma when setting itables.options.columnDefs (#601)"""
COLUMN_DEFS_IN_A_TUPLE = ([{"className": "dt-center", "targets": "_all"}],)


def test_warns_on_column_defs_in_a_tuple(df):
    # every item of a collection is checked, not just the first one, and the
    # option is reported as the user wrote it, i.e. before itables adds its
    # own column definitions to it (#601)
    with pytest.warns(
        SyntaxWarning,
        match=re.escape(f"columnDefs={COLUMN_DEFS_IN_A_TUPLE} does not match"),
    ):
        with pytest.raises(TypeError, match="extra list or tuple"):
            itables.to_html_datatable(df, columnDefs=COLUMN_DEFS_IN_A_TUPLE)  # type: ignore


def test_raises_on_column_defs_in_a_tuple(df):
    # itables reads and completes the column definitions, so unlike most
    # DataTables options they can't just be passed on as they are (#601)
    with pytest.warns(SyntaxWarning):
        with pytest.raises(
            TypeError, match=re.escape("must be a sequence of column definitions")
        ):
            itables.to_html_datatable(df, columnDefs=COLUMN_DEFS_IN_A_TUPLE)  # type: ignore


def test_warns_when_an_option_is_set(monkeypatch):
    # options are checked when they are set, so that the warning points at
    # the assignment rather than at the next table (#601)
    with pytest.warns(
        SyntaxWarning,
        match=re.escape(f"columnDefs={COLUMN_DEFS_IN_A_TUPLE} does not match"),
    ):
        monkeypatch.setattr(
            itables.options, "columnDefs", COLUMN_DEFS_IN_A_TUPLE, raising=False
        )


def test_warns_when_an_undocumented_option_is_set(monkeypatch):
    with pytest.warns(
        SyntaxWarning,
        match="These arguments are not documented in ITableOptions: .*'lengthMenuWithTypo'",
    ):
        monkeypatch.setattr(
            itables.options, "lengthMenuWithTypo", [2, 5, 10], raising=False
        )


def test_no_warning_when_a_valid_option_is_set(monkeypatch):
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        monkeypatch.setattr(itables.options, "lengthMenu", [2, 5, 10], raising=False)
