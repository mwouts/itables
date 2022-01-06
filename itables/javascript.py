"""HTML/js representation of Pandas dataframes"""

import io
import json
import logging
import os
import re
import uuid
import warnings

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


def replace_value(template, pattern, value, count=1):
    """Set the given pattern to the desired value in the template,
    after making sure that the pattern is found exactly once."""
    assert isinstance(template, str)
    assert template.count(pattern) == count
    return template.replace(pattern, value)


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
    eval_functions = kwargs.pop("eval_functions", None)

    if isinstance(df, (np.ndarray, np.generic)):
        df = pd.DataFrame(df)

    if isinstance(df, pd.Series):
        df = df.to_frame()

    df = downsample(df, max_rows=maxRows, max_columns=maxColumns, max_bytes=maxBytes)

    # Do not show the page menu when the table has fewer rows than min length menu
    if "paging" not in kwargs and len(df.index) <= kwargs.get("lengthMenu", [10])[0]:
        kwargs["paging"] = False

    # Load the HTML template
    output = read_package_file("datatables_template.html")

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
    table_header = (
        f'<table id="{tableId}" class="{classes}"><thead>{thead}</thead></table>'
    )
    output = replace_value(
        output,
        '<table id="table_id"><thead><tr><th>A</th></tr></thead></table>',
        table_header,
    )
    output = replace_value(output, "#table_id", f"#{tableId}", count=2)

    # Export the DT args to JSON
    dt_args = json.dumps(kwargs)

    # And load the eval_functions_js library if required
    if eval_functions:
        eval_functions_js = read_package_file("javascript", "eval_functions.js")
        output = replace_value(
            output,
            "// eval_functions_js",
            f"<script>\n{eval_functions_js}\n<script>",
        )
        output = replace_value(
            output,
            "let dt_args = {};",
            f"let dt_args = eval_functions({dt_args});",
        )
    else:
        output = replace_value(output, "let dt_args = {};", f"let dt_args = {dt_args};")
        if eval_functions is None and _any_function(kwargs):
            warnings.warn(
                "One of the arguments passed to datatables starts with 'function'. "
                "To evaluate this function, use the option 'eval_functions=True'. "
                "To silence this warning, use 'eval_functions=False'."
            )

    # Export the table data to JSON and include this in the HTML
    data = _formatted_values(df.reset_index() if showIndex else df)
    dt_data = json.dumps(data)
    output = replace_value(output, "const data = [];", f"const data = {dt_data};")

    return output


def _any_function(value):
    """Does a value or nested value starts with 'function'?"""
    if isinstance(value, str) and value.startswith("function"):
        return True
    elif isinstance(value, list):
        for nested_value in value:
            if _any_function(nested_value):
                return True
    elif isinstance(value, dict):
        for key, nested_value in value.items():
            if _any_function(nested_value):
                return True
    return False


def show(df=None, **kwargs):
    """Show a dataframe"""
    html = _datatables_repr_(df, **kwargs)
    load_datatables(skip_if_already_loaded=True)
    display(HTML(html))
