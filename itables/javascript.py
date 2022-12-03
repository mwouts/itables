"""HTML/js representation of Pandas dataframes"""

import json
import logging
import re
import uuid
import warnings
from base64 import b64encode

import numpy as np
import pandas as pd
from IPython.display import HTML, Javascript, display
from six import string_types

import itables.options as opt

from .datatables_format import datatables_rows
from .downsample import downsample
from .utils import read_package_file

logging.basicConfig()
logger = logging.getLogger(__name__)

_ORIGINAL_DATAFRAME_REPR_HTML = pd.DataFrame._repr_html_
_CONNECTED = True

try:
    import google.colab

    # I can't find out how to suppress the LGTM alert about unused-import
    # (Tried with # lgtm[py/unused-import]  # noqa: F401)
    # So we use the import:
    assert google.colab.output

    GOOGLE_COLAB = True
except ImportError:
    GOOGLE_COLAB = False


def init_notebook_mode(
    all_interactive=False, connected=GOOGLE_COLAB, warn_if_call_is_superfluous=True
):
    """Load the datatables.net library and the corresponding css (if connected=False),
    and (if all_interactive=True), activate the datatables representation for all the Pandas DataFrames and Series.

    Warning: make sure you keep the output of this cell when 'connected=False',
    otherwise the interactive tables will stop working.
    """
    global _CONNECTED
    if GOOGLE_COLAB and not connected:
        warnings.warn(
            "The offline mode for itables is not supposed to work in Google Colab. "
            "This is because HTML outputs in Google Colab are encapsulated in iframes."
        )

    if (
        all_interactive is False
        and pd.DataFrame._repr_html_ == _ORIGINAL_DATAFRAME_REPR_HTML
        and connected is True
        and _CONNECTED == connected
    ):
        if warn_if_call_is_superfluous:
            warnings.warn(
                "Did you know? "
                "init_notebook_mode(all_interactive=False, connected=True) does nothing. "
                "Feel free to remove this line, or pass warn_if_call_is_superfluous=False."
            )
        return

    _CONNECTED = connected

    if all_interactive:
        pd.DataFrame._repr_html_ = _datatables_repr_
        pd.Series._repr_html_ = _datatables_repr_
    else:
        pd.DataFrame._repr_html_ = _ORIGINAL_DATAFRAME_REPR_HTML
        if hasattr(pd.Series, "_repr_html_"):
            del pd.Series._repr_html_

    if not connected:
        display(Javascript(read_package_file("external/jquery.min.js")))
        # We use datatables' ES module version because the non module version
        # fails to load as a simple script in the presence of require.js
        dt64 = b64encode(
            read_package_file("external/jquery.dataTables.mjs").encode("utf-8")
        ).decode("ascii")
        display(
            HTML(
                replace_value(
                    read_package_file("html/itables_render.html"),
                    "dt_src",
                    "data:text/javascript;base64,{}".format(dt64),
                )
            )
        )
        display(
            HTML(
                "<style>"
                + read_package_file("external/jquery.dataTables.min.css")
                + "</style>"
            )
        )


def _table_header(
    df, table_id, show_index, classes, style, tags, footer, column_filters
):
    """This function returns the HTML table header. Rows are not included."""
    # Generate table head using pandas.to_html(), see issue 63
    pattern = re.compile(r".*<thead>(.*)</thead>", flags=re.MULTILINE | re.DOTALL)
    match = pattern.match(df.head(0).to_html())
    thead = match.groups()[0]
    if not show_index:
        thead = thead.replace("<th></th>", "", 1)

    if column_filters:
        # We use this header in the column filters, so we need to remove any column multiindex first"""
        thead_flat = ""
        if show_index:
            for index in df.index.names:
                thead_flat += "<th>{}</th>".format(index)

        for column in df.columns:
            thead_flat += "<th>{}</th>".format(column)

    loading = "<td>Loading... (need <a href=https://mwouts.github.io/itables/troubleshooting.html>help</a>?)</td>"
    tbody = "<tr>{}</tr>".format(loading)

    if style:
        style = 'style="{}"'.format(style)
    else:
        style = ""

    if column_filters == "header":
        header = "<thead>{}</thead>".format(thead_flat)
    else:
        header = "<thead>{}</thead>".format(thead)

    if column_filters == "footer":
        footer = "<tfoot>{}</tfoot>".format(thead_flat)
    elif footer:
        footer = "<tfoot>{}</tfoot>".format(thead)
    else:
        footer = ""

    return """<table id="{table_id}" class="{classes}"{style}>{tags}{header}<tbody>{tbody}</tbody>{footer}</table>""".format(
        table_id=table_id,
        classes=classes,
        style=style,
        tags=tags,
        header=header,
        tbody=tbody,
        footer=footer,
    )


def json_dumps(obj, eval_functions):
    """
    This is a replacement for json.dumps that
    does not quote strings that start with 'function', so that
    these functions are evaluated in the HTML code.
    """
    if isinstance(obj, JavascriptFunction):
        assert obj.lstrip().startswith("function")
        return obj
    if isinstance(obj, str) and obj.lstrip().startswith("function"):
        if eval_functions is True:
            return obj
        if eval_functions is None and obj.lstrip().startswith("function"):
            warnings.warn(
                "One of the arguments passed to datatables starts with 'function'. "
                "To evaluate this function, change it into a 'JavascriptFunction' object "
                "or use the option 'eval_functions=True'. "
                "To silence this warning, use 'eval_functions=False'."
            )
    if isinstance(obj, list):
        return "[" + ", ".join(json_dumps(i, eval_functions) for i in obj) + "]"
    if isinstance(obj, dict):
        return (
            "{"
            + ", ".join(
                '"{}": {}'.format(key, json_dumps(value, eval_functions))
                for key, value in obj.items()
            )
            + "}"
        )
    return json.dumps(obj)


def replace_value(template, pattern, value):
    """Set the given pattern to the desired value in the template,
    after making sure that the pattern is found exactly once."""
    assert isinstance(template, string_types)
    assert template.count(pattern) == 1
    return template.replace(pattern, value)


class JavascriptFunction(str):
    """A class that explicitly states that a string is a Javascript function"""

    def __init__(self, value):
        assert value.lstrip().startswith(
            "function"
        ), "A Javascript function is expected to start with 'function'"


def _datatables_repr_(df=None, tableId=None, **kwargs):
    return to_html_datatable(df, tableId, connected=_CONNECTED, **kwargs)


def to_html_datatable(df=None, caption=None, tableId=None, connected=True, **kwargs):
    """Return the HTML representation of the given dataframe as an interactive datatable"""
    # Default options
    for option in dir(opt):
        if (
            option not in kwargs
            and not option.startswith("__")
            and option not in ["read_package_file", "warn_on_unexpected_types"]
        ):
            kwargs[option] = getattr(opt, option)

    # These options are used here, not in DataTable
    classes = kwargs.pop("classes")
    style = kwargs.pop("style")
    css = kwargs.pop("css")
    tags = kwargs.pop("tags")

    if caption is not None:
        tags = '{}<caption style="white-space: nowrap; overflow: hidden">{}</caption>'.format(
            tags, caption
        )

    showIndex = kwargs.pop("showIndex")
    maxBytes = kwargs.pop("maxBytes", 0)
    maxRows = kwargs.pop("maxRows", 0)
    maxColumns = kwargs.pop("maxColumns", pd.get_option("display.max_columns") or 0)
    eval_functions = kwargs.pop("eval_functions", None)
    pre_dt_code = kwargs.pop("pre_dt_code")

    if isinstance(df, (np.ndarray, np.generic)):
        df = pd.DataFrame(df)

    if isinstance(df, pd.Series):
        df = df.to_frame()

    if showIndex == "auto":
        showIndex = df.index.name is not None or not isinstance(df.index, pd.RangeIndex)

    df, downsampling_warning = downsample(
        df, max_rows=maxRows, max_columns=maxColumns, max_bytes=maxBytes
    )

    if downsampling_warning and "fnInfoCallback" not in kwargs:
        kwargs["fnInfoCallback"] = JavascriptFunction(
            "function (oSettings, iStart, iEnd, iMax, iTotal, sPre) {{ return sPre + ' ({warning})'; }}".format(
                warning=downsampling_warning
            )
        )

    footer = kwargs.pop("footer")
    column_filters = kwargs.pop("column_filters")
    if column_filters == "header":
        pass
    elif column_filters == "footer":
        footer = True
    elif column_filters is not False:
        raise ValueError(
            "column_filters should be either "
            "'header', 'footer' or False, not {}".format(column_filters)
        )

    # Do not show the page menu when the table has fewer rows than min length menu
    if "paging" not in kwargs and len(df.index) <= kwargs.get("lengthMenu", [10])[0]:
        kwargs["paging"] = False

    # Load the HTML template
    if connected:
        output = read_package_file("html/datatables_template_connected.html")
    else:
        output = read_package_file("html/datatables_template.html")

    tableId = tableId or str(uuid.uuid4())
    if isinstance(classes, list):
        classes = " ".join(classes)

    if not showIndex:
        df = df.set_index(pd.RangeIndex(len(df.index)))

    table_header = _table_header(
        df, tableId, showIndex, classes, style, tags, footer, column_filters
    )
    output = replace_value(
        output,
        '<table id="table_id"><thead><tr><th>A</th></tr></thead></table>',
        table_header,
    )
    output = replace_value(output, "#table_id", "#{}".format(tableId))
    output = replace_value(
        output,
        "<style></style>",
        "<style>{}</style>".format(css),
    )

    if column_filters:
        # If the below was false, we would need to concatenate the JS code
        # which might not be trivial...
        assert pre_dt_code == ""
        assert "initComplete" not in kwargs

        pre_dt_code = replace_value(
            read_package_file("html/column_filters/pre_dt_code.js"),
            "thead_or_tfoot",
            "thead" if column_filters == "header" else "tfoot",
        )
        kwargs["initComplete"] = JavascriptFunction(
            replace_value(
                replace_value(
                    read_package_file("html/column_filters/initComplete.js"),
                    "const initComplete = ",
                    "",
                ),
                "header",
                column_filters,
            )
        )

    # Export the DT args to JSON
    dt_args = json_dumps(kwargs, eval_functions)

    output = replace_value(
        output, "let dt_args = {};", "let dt_args = {};".format(dt_args)
    )
    output = replace_value(
        output,
        "// [pre-dt-code]",
        pre_dt_code.replace("#table_id", "#{}".format(tableId)),
    )

    # Export the table data to JSON and include this in the HTML
    if showIndex:
        df = safe_reset_index(df)

    dt_data = datatables_rows(df)

    output = replace_value(
        output, "const data = [];", "const data = {};".format(dt_data)
    )

    return output


def safe_reset_index(df):
    try:
        return df.reset_index()
    except ValueError:
        # Issue #134: the above might fail if the index has duplicated names or if one of the
        # index names is already a column, with e.g "ValueError: cannot insert A, already exists"
        index_levels = [
            pd.Series(
                df.index.get_level_values(i),
                name=name
                or (
                    "index{}".format(i)
                    if isinstance(df.index, pd.MultiIndex)
                    else "index"
                ),
            )
            for i, name in enumerate(df.index.names)
        ]
        return pd.concat(index_levels + [df.reset_index(drop=True)], axis=1)


def show(df=None, caption=None, **kwargs):
    """Show a dataframe"""
    html = to_html_datatable(df, caption=caption, connected=_CONNECTED, **kwargs)
    display(HTML(html))
