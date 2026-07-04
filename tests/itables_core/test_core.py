"""Test the core functions shared by pydatatables and pyaggrid"""

import json

import pytest
from itables_core.downsample import as_nbytes, downsample, nbytes
from itables_core.formatting import datatables_rows, get_keys_to_be_evaluated
from itables_core.frames import evaluate_show_index, safe_reset_index
from itables_core.typing import JavascriptCode, JavascriptFunction

pd = pytest.importorskip("pandas")


def test_as_nbytes():
    assert as_nbytes("64KB") == 64 * 2**10
    assert as_nbytes("1MB") == 2**20
    assert as_nbytes(1000) == 1000


def test_downsample_max_rows():
    df = pd.DataFrame({"a": range(100)})
    small, warning = downsample(df, max_rows=10)
    assert len(small) == 10
    assert "downsampled" in warning
    # first and last rows are preserved
    assert small["a"].iloc[0] == 0
    assert small["a"].iloc[-1] == 99


def test_downsample_max_bytes():
    df = pd.DataFrame({"a": range(10000)})
    small, warning = downsample(df, max_bytes=1000)
    assert nbytes(small) <= 1000
    assert "downsampled" in warning


def test_no_downsampling_when_below_limits():
    df = pd.DataFrame({"a": range(5)})
    same, warning = downsample(df, max_rows=100, max_bytes="64KB")
    assert len(same) == 5
    assert warning == ""


def test_datatables_rows():
    df = pd.DataFrame({"a": [1, 2], "b": ["x", "<z>"]})
    data = json.loads(datatables_rows(df))
    assert data == [[1, "x"], [2, "&lt;z&gt;"]]


def test_datatables_rows_not_escaped():
    df = pd.DataFrame({"b": ["<z>"]})
    data = json.loads(datatables_rows(df, escape_html=False))
    assert data == [["<z>"]]


def test_non_finite_floats_are_encoded():
    df = pd.DataFrame({"a": [1.5, float("nan"), float("inf")]})
    data = json.loads(datatables_rows(df, escape_html=False))
    assert data == [[1.5], ["___NaN___"], ["___Infinity___"]]


def test_get_keys_to_be_evaluated():
    args = {
        "getRowStyle": JavascriptFunction("function (params) { return null; }"),
        "nested": {"code": JavascriptCode("window.foo")},
        "plain": "not evaluated",
    }
    keys = get_keys_to_be_evaluated(args)
    assert sorted(keys) == [["getRowStyle"], ["nested", "code"]]


def test_evaluate_show_index():
    df = pd.DataFrame({"a": [1, 2]})
    assert evaluate_show_index(df, "auto") is False
    assert evaluate_show_index(df, True) is True

    df_named = df.set_axis(pd.Index(["x", "y"], name="idx"))
    assert evaluate_show_index(df_named, "auto")


def test_safe_reset_index():
    df = pd.DataFrame({"a": [1, 2]}, index=pd.Index(["x", "y"], name="idx"))
    reset = safe_reset_index(df)
    assert list(reset.columns) == ["idx", "a"]
