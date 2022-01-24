"""HTML/js representation of Pandas dataframes"""

import json
import logging
import uuid
import warnings

import numpy as np
import pandas as pd
import pandas.io.formats.format as fmt
from IPython.core.display import HTML, Javascript, display

import itables.options as opt

from .downsample import downsample
from .utils import read_package_file

logging.basicConfig()
logger = logging.getLogger(__name__)

_ORIGINAL_DATAFRAME_REPR_HTML = pd.DataFrame._repr_html_


def init_notebook_mode(all_interactive=False):
    """Load the datatables.net library and the corresponding css, and if desired (all_interactive=True),
    activate the datatables representation for all the Pandas DataFrames and Series.

    Make sure you don't remove the output of this cell, otherwise the interactive tables won't work when
    your notebook is reloaded.
    """
    if all_interactive:
        pd.DataFrame._repr_html_ = _datatables_repr_
        pd.Series._repr_html_ = _datatables_repr_
    else:
        pd.DataFrame._repr_html_ = _ORIGINAL_DATAFRAME_REPR_HTML
        if hasattr(pd.Series, "_repr_html_"):
            del pd.Series._repr_html_

    # TODO remove this when require.js is not used any more, see #51
    display(Javascript(read_package_file("require_config.js")))


def _formatted_values(df):
    """Return the table content as a list of lists for DataTables"""
    formatted_df = df.copy()
    for col in formatted_df:
        x = formatted_df[col]
        if x.dtype.kind in ["b", "i", "s"]:
            continue

        if x.dtype.kind == "O":
            formatted_df[col] = formatted_df[col].astype(str)
            continue

        formatted_df[col] = np.array(fmt.format_array(x.values, None))
        if x.dtype.kind == "f":
            try:
                formatted_df[col] = formatted_df[col].astype(np.float)
            except ValueError:
                pass

    return formatted_df.values.tolist()


def _table_header(df, table_id, show_index, classes, style):
    """This function returns the HTML table header. Rows are not included."""
    thead = ""
    if show_index:
        thead = "<th></th>" * len(df.index.names)

    for column in df.columns:
        thead += f"<th>{column}</th>"

    loading = "<td>Loading... (need <a href=https://mwouts.github.io/itables/troubleshooting.html>help</a>?)</td>"
    tbody = f"<tr>{loading}</tr>"

    if style:
        style = f'style="{style}"'
    else:
        style = ""

    return f'<table id="{table_id}" class="{classes}"{style}><thead>{thead}</thead><tbody>{tbody}</tbody></table>'


def eval_functions_dumps(obj):
    """
    This is a replacement for json.dumps that
    does not quote strings that start with 'function', so that
    these functions are evaluated in the HTML code.
    """
    if isinstance(obj, str):
        if obj.lstrip().startswith("function"):
            return obj
    if isinstance(obj, list):
        return "[" + ", ".join(eval_functions_dumps(i) for i in obj) + "]"
    if isinstance(obj, dict):
        return (
            "{"
            + ", ".join(
                f'"{key}": {eval_functions_dumps(value)}' for key, value in obj.items()
            )
            + "}"
        )
    return json.dumps(obj)


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
    style = kwargs.pop("style")
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

    table_header = _table_header(df, tableId, showIndex, classes, style)
    output = replace_value(
        output,
        '<table id="table_id"><thead><tr><th>A</th></tr></thead></table>',
        table_header,
    )
    output = replace_value(output, "#table_id", f"#{tableId}", count=2)

    # Export the DT args to JSON
    if eval_functions:
        dt_args = eval_functions_dumps(kwargs)
    else:
        dt_args = json.dumps(kwargs)
        if eval_functions is None and _any_function(kwargs):
            warnings.warn(
                "One of the arguments passed to datatables starts with 'function'. "
                "To evaluate this function, use the option 'eval_functions=True'. "
                "To silence this warning, use 'eval_functions=False'."
            )

    output = replace_value(
        output, "let dt_args = {};", f"let dt_args = {dt_args};", count=2
    )

    # Export the table data to JSON and include this in the HTML
    data = _formatted_values(df.reset_index() if showIndex else df)
    dt_data = json.dumps(data)
    output = replace_value(output, "const data = [];", f"const data = {dt_data};")

    return output


def _any_function(value):
    """Does a value or nested value starts with 'function'?"""
    if isinstance(value, str) and value.lstrip().startswith("function"):
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
    display(HTML(html))
