import json
import warnings

import pandas as pd
import pytest

from itables import JavascriptFunction, show
from itables.javascript import json_dumps


@pytest.fixture()
def df():
    return pd.DataFrame([[-1, 2, -3, 4, -5], [6, -7, 8, -9, 10]], columns=list("abcde"))


@pytest.fixture()
def coloredColumnDefs():
    return [
        {
            "targets": "_all",
            "createdCell": """function (td, cellData, rowData, row, col) {
              if ( cellData < 0 ) {
                $(td).css('color', 'red')
              }
            }""",
        }
    ]


def test_warning_when_eval_functions_is_missing(df, coloredColumnDefs, connected):
    with pytest.warns(UserWarning, match="starts with 'function'"):
        show(df, connected=connected, columnDefs=coloredColumnDefs)


def test_no_warning_when_eval_functions_is_false(df, coloredColumnDefs, connected):
    warnings.simplefilter("error")
    show(df, connected=connected, columnDefs=coloredColumnDefs, eval_functions=False)


def test_no_warning_when_eval_functions_is_true(df, coloredColumnDefs, connected):
    warnings.simplefilter("error")
    show(df, connected=connected, columnDefs=coloredColumnDefs, eval_functions=True)


@pytest.mark.parametrize("obj", ["a", 1, 1.0, [1.0, "a", {"a": [0, 1]}]])
def test_our_json_dumps_same_as_json_dumps(obj):
    warnings.simplefilter("error")
    assert json_dumps(obj, eval_functions=True) == json.dumps(obj)


def test_json_dumps():
    warnings.simplefilter("error")
    assert json_dumps("not a function", eval_functions=True) == '"not a function"'
    assert (
        json_dumps("function(x) {return x;}", eval_functions=True)
        == "function(x) {return x;}"
    )
    assert (
        json_dumps(JavascriptFunction("function(x) {return x;}"), eval_functions=False)
        == "function(x) {return x;}"
    )
    assert (
        json_dumps(["a", "function(x) {return x;}"], eval_functions=True)
        == '["a", function(x) {return x;}]'
    )
    assert (
        json_dumps({"f": "function(x) {return x;}"}, eval_functions=True)
        == '{"f": function(x) {return x;}}'
    )


def test_json_dumps_issues_warnings():
    with pytest.warns(UserWarning, match="starts with 'function'"):
        json_dumps("function(x) {return x;}", eval_functions=None)
