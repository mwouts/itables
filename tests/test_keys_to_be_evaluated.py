import pytest

from itables.javascript import JavascriptFunction, get_keys_to_be_evaluated


@pytest.fixture()
def coloredColumnDefs():
    return [
        {
            "targets": "_all",
            "createdCell": JavascriptFunction(
                "function (td, cellData, rowData, row, col) {if (cellData<0) {$(td).css('color', 'red')}}"
            ),
        }
    ]


def test_get_keys_to_be_evaluated(coloredColumnDefs):
    keys_to_be_evaluated = get_keys_to_be_evaluated({"columnDefs": coloredColumnDefs})

    assert keys_to_be_evaluated == [["columnDefs", 0, "createdCell"]]
