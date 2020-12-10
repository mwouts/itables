"""HTML/js representation of Pandas dataframes"""

import io
import json
import logging
import os
import re
import uuid

import numpy as np
import pandas as pd
import pandas.io.formats.format as fmt
from IPython.core.display import HTML, Javascript, display

import itables.options as opt

from .downsample import downsample

try:
    unicode  # Python 2
except NameError:
    unicode = str  # Python 3

logging.basicConfig()
logger = logging.getLogger(__name__)

_DATATABLE_LOADED = False


def read_package_file(*path):
    current_path = os.path.dirname(__file__)
    with io.open(os.path.join(current_path, *path), encoding="utf-8") as fp:
        return fp.read()


def init_notebook_mode(all_interactive=False):
    """Load the datatables.net library and the corresponding css, and if desired (all_interactive=True),
    activate the datatables representation for all the Pandas DataFrames and Series.

    Make sure you don't remove the output of this cell, otherwise the interactive tables won't work when
    your notebook is reloaded.
    """
    if all_interactive:
        pd.DataFrame._repr_html_ = _datatables_repr_
        pd.Series._repr_html_ = _datatables_repr_

    load_datatables(skip_if_already_loaded=False)


def load_datatables(skip_if_already_loaded=True):
    global _DATATABLE_LOADED
    if _DATATABLE_LOADED and skip_if_already_loaded:
        return

    load_datatables_js = read_package_file("javascript", "load_datatables_connected.js")
    eval_functions_js = read_package_file("javascript", "eval_functions.js")
    load_datatables_js += (
        "\n$('head').append(`<script>\n" + eval_functions_js + "\n</` + 'script>');"
    )

    display(Javascript(load_datatables_js))

    _DATATABLE_LOADED = True


def _formatted_values(df):
    """Return the table content as a list of lists for DataTables"""
    formatted_df = df.copy()
    for col in formatted_df:
        x = formatted_df[col]
        if x.dtype.kind in ["b", "i", "s"]:
            continue

        if x.dtype.kind == "O":
            formatted_df[col] = formatted_df[col].astype(unicode)
            continue

        formatted_df[col] = np.array(fmt.format_array(x.values, None))
        if x.dtype.kind == "f":
            try:
                formatted_df[col] = formatted_df[col].astype(np.float)
            except ValueError:
                pass

    return formatted_df.values.tolist()


def _datatables_repr_(df=None, tableId=None, **kwargs):
    """Return the HTML/javascript representation of the table"""

    # Default options
    for option in dir(opt):
        if option not in kwargs and not option.startswith("__"):
            kwargs[option] = getattr(opt, option)

    # These options are used here, not in DataTable
    classes = kwargs.pop("classes")
    showIndex = kwargs.pop("showIndex")
    maxBytes = kwargs.pop("maxBytes", 0)
    maxRows = kwargs.pop("maxRows", 0)
    maxColumns = kwargs.pop("maxColumns", pd.get_option("display.max_columns") or 0)

    if isinstance(df, (np.ndarray, np.generic)):
        df = pd.DataFrame(df)

    if isinstance(df, pd.Series):
        df = df.to_frame()

    df = downsample(df, max_rows=maxRows, max_columns=maxColumns, max_bytes=maxBytes)

    # Do not show the page menu when the table has fewer rows than min length menu
    if "paging" not in kwargs and len(df.index) <= kwargs.get("lengthMenu", [10])[0]:
        kwargs["paging"] = False

    tableId = tableId or str(uuid.uuid4())
    if isinstance(classes, list):
        classes = " ".join(classes)

    if showIndex == "auto":
        showIndex = df.index.name is not None or not isinstance(df.index, pd.RangeIndex)

    if not showIndex:
        df = df.set_index(pd.RangeIndex(len(df.index)))

    # Generate table head using pandas.to_html()
    pattern = re.compile(r".*<thead>(.*)</thead>", flags=re.MULTILINE | re.DOTALL)
    match = pattern.match(df.head(0).to_html())
    thead = match.groups()[0]
    if not showIndex:
        thead = thead.replace("<th></th>", "", 1)
    html_table = (
        '<table id="'
        + tableId
        + '" class="'
        + classes
        + '"><thead>'
        + thead
        + "</thead></table>"
    )

    kwargs["data"] = _formatted_values(df.reset_index() if showIndex else df)

    try:
        dt_args = json.dumps(kwargs)
        return (
            """<div>"""
            + html_table
            + """
<script type="text/javascript">
require(["datatables"], function (datatables) {
    $(document).ready(function () {
        var dt_args = """
            + dt_args
            + """;
        dt_args = eval_functions(dt_args);
        table = $('#"""
            + tableId
            + """').DataTable(dt_args);
    });
})
</script>
</div>
"""
        )
    except TypeError as error:
        logger.error(str(error))
        return ""


def show(df=None, **kwargs):
    """Show a dataframe"""
    html = _datatables_repr_(df, **kwargs)
    load_datatables(skip_if_already_loaded=True)
    display(HTML(html))
