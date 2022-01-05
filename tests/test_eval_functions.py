import warnings

import pandas as pd
import pytest

from itables import show


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


def test_warning_when_eval_functions_is_missing(df, coloredColumnDefs):
    with pytest.warns(UserWarning, match="starts with 'function'"):
        show(df, columnDefs=coloredColumnDefs)


def test_no_warning_when_eval_functions_is_false(df, coloredColumnDefs):
    warnings.simplefilter("error")
    show(df, columnDefs=coloredColumnDefs, eval_functions=False)


def test_no_warning_when_eval_functions_is_true(df, coloredColumnDefs):
    warnings.simplefilter("error")
    show(df, columnDefs=coloredColumnDefs, eval_functions=True)
