import re
import warnings
from typing import Any

import pytest

import itables
from itables.javascript import get_itable_arguments

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


DATATABLE_CALLBACKS = [
    "createdRow",
    "footerCallback",
    "formatNumber",
    "headerCallback",
    "infoCallback",
    "preDrawCallback",
    "rowCallback",
    "stateLoadCallback",
    "stateLoadParams",
    "stateLoaded",
    "stateSaveCallback",
    "stateSaveParams",
]


@pytest.mark.parametrize("option_name", DATATABLE_CALLBACKS)
@pytest.mark.parametrize("global_default", [False, True])
def test_datatables_callback_is_accepted(df, monkeypatch, option_name, global_default):
    callback = itables.JavascriptFunction("function () { return true; }")
    with warnings.catch_warnings():
        warnings.simplefilter("error", SyntaxWarning)
        if global_default:
            monkeypatch.setattr(itables.options, option_name, callback, raising=False)
            args = get_itable_arguments(df)
        else:
            kwargs: dict[str, Any] = {option_name: callback}
            args = get_itable_arguments(df, **kwargs)
    assert args[option_name] == callback
    assert "keys_to_be_evaluated" in args
    assert [option_name] in args["keys_to_be_evaluated"]


@pytest.mark.parametrize("option_name", DATATABLE_CALLBACKS)
def test_datatables_callback_requires_javascript_function(df, option_name):
    with pytest.warns(SyntaxWarning, match=option_name + ".*does not match"):
        kwargs: dict[str, Any] = {option_name: "function () {}"}
        itables.to_html_datatable(df, **kwargs)
