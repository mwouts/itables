"""HTML/js representation of Pandas dataframes"""

import json
import logging
import re
import sys
import uuid
import warnings
from base64 import b64encode

import numpy as np
import pandas as pd
import pandas.io.formats.style as pd_style

try:
    import polars as pl
except ImportError:
    # Define pl.Series as pd.Series
    import pandas as pl

from IPython.display import HTML, Javascript, display

import itables.options as opt

from .datatables_format import datatables_rows
from .downsample import downsample
from .utils import read_package_file

logging.basicConfig()
logger = logging.getLogger(__name__)

_OPTIONS_NOT_AVAILABLE_WITH_TO_HTML = {
    "tags",
    "footer",
    "column_filters",
    "maxBytes",
    "maxRows",
    "maxColumns",
    "warn_on_unexpected_types",
    "warn_on_int_to_str_conversion",
}
_ORIGINAL_DATAFRAME_REPR_HTML = pd.DataFrame._repr_html_
_ORIGINAL_DATAFRAME_STYLE_REPR_HTML = pd_style.Styler._repr_html_
_ORIGINAL_POLARS_DATAFRAME_REPR_HTML = pl.DataFrame._repr_html_
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
        pd_style.Styler._repr_html_ = _datatables_repr_
        pl.DataFrame._repr_html_ = _datatables_repr_
        pl.Series._repr_html_ = _datatables_repr_
    else:
        pd.DataFrame._repr_html_ = _ORIGINAL_DATAFRAME_REPR_HTML
        pd_style.Styler._repr_html_ = _ORIGINAL_DATAFRAME_STYLE_REPR_HTML
        pl.DataFrame._repr_html_ = _ORIGINAL_POLARS_DATAFRAME_REPR_HTML
        if hasattr(pd.Series, "_repr_html_"):
            del pd.Series._repr_html_
        if hasattr(pl.Series, "_repr_html_"):
            del pl.Series._repr_html_

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
                    read_package_file("html/initialize_offline_datatable.html"),
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
    try:
        html_header = df.head(0).to_html()
    except AttributeError:
        # Polars DataFrames
        html_header = pd.DataFrame(data=[], columns=df.columns).to_html()
    match = pattern.match(html_header)
    thead = match.groups()[0]
    # Don't remove the index header for empty dfs
    if not show_index and len(df.columns):
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
    if isinstance(obj, JavascriptCode):
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
    if sys.version_info >= (3,):
        assert isinstance(template, str)
    count = template.count(pattern)
    if not count:
        raise ValueError("pattern={} was not found in template".format(pattern))
    elif count > 1:
        raise ValueError(
            "pattern={} was found multiple times ({}) in template".format(
                pattern, count
            )
        )
    return template.replace(pattern, value)


class JavascriptFunction(str):
    """A class that explicitly states that a string is a Javascript function"""

    def __init__(self, value):
        assert value.lstrip().startswith(
            "function"
        ), "A Javascript function is expected to start with 'function'"


class JavascriptCode(str):
    """A class that explicitly states that a string is a Javascript code"""

    pass


def _datatables_repr_(df):
    return to_html_datatable(df, connected=_CONNECTED)


def to_html_datatable(
    df=None,
    caption=None,
    tableId=None,
    connected=True,
    import_jquery=True,
    use_to_html=False,
    **kwargs
):
    if use_to_html or isinstance(df, pd_style.Styler):
        return to_html_datatable_using_to_html(
            df=df,
            caption=caption,
            tableId=tableId,
            connected=connected,
            import_jquery=import_jquery,
            **kwargs
        )

    """Return the HTML representation of the given dataframe as an interactive datatable"""
    set_default_options(kwargs, use_to_html=False)

    # These options are used here, not in DataTable
    classes = kwargs.pop("classes")
    style = kwargs.pop("style")
    tags = kwargs.pop("tags")

    if caption is not None:
        tags = '{}<caption style="white-space: nowrap; overflow: hidden">{}</caption>'.format(
            tags, caption
        )

    showIndex = kwargs.pop("showIndex")

    if isinstance(df, (np.ndarray, np.generic)):
        df = pd.DataFrame(df)

    if isinstance(df, (pd.Series, pl.Series)):
        df = df.to_frame()

    if showIndex == "auto":
        try:
            showIndex = df.index.name is not None or not isinstance(
                df.index, pd.RangeIndex
            )
        except AttributeError:
            # Polars DataFrame
            showIndex = False

    maxBytes = kwargs.pop("maxBytes", 0)
    maxRows = kwargs.pop("maxRows", 0)
    maxColumns = kwargs.pop("maxColumns", pd.get_option("display.max_columns") or 0)
    warn_on_unexpected_types = kwargs.pop("warn_on_unexpected_types", False)
    warn_on_int_to_str_conversion = kwargs.pop("warn_on_int_to_str_conversion", False)

    df, downsampling_warning = downsample(
        df, max_rows=maxRows, max_columns=maxColumns, max_bytes=maxBytes
    )

    if downsampling_warning and "fnInfoCallback" not in kwargs:
        kwargs["fnInfoCallback"] = JavascriptFunction(
            "function (oSettings, iStart, iEnd, iMax, iTotal, sPre) {{ return sPre + ' ({warning})'; }}".format(
                warning=downsampling_warning
            )
        )

    if "dom" not in kwargs and _df_fits_in_one_page(df, kwargs):
        kwargs["dom"] = "ti" if downsampling_warning else "t"

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

    tableId = tableId or str(uuid.uuid4())
    if isinstance(classes, list):
        classes = " ".join(classes)

    if not showIndex:
        try:
            df = df.set_index(pd.RangeIndex(len(df.index)))
        except AttributeError:
            # Polars DataFrames
            pass

    table_header = _table_header(
        df, tableId, showIndex, classes, style, tags, footer, column_filters
    )

    # Export the table data to JSON and include this in the HTML
    if showIndex:
        df = safe_reset_index(df)

    # When the header has an extra column, we add
    # an extra empty column in the table data #141
    column_count = _column_count_in_header(table_header)
    dt_data = datatables_rows(
        df,
        column_count,
        warn_on_unexpected_types=warn_on_unexpected_types,
        warn_on_int_to_str_conversion=warn_on_int_to_str_conversion,
    )

    return html_table_from_template(
        table_header,
        table_id=tableId,
        data=dt_data,
        kwargs=kwargs,
        connected=connected,
        import_jquery=import_jquery,
        column_filters=column_filters,
    )


def set_default_options(kwargs, use_to_html):
    if use_to_html:
        options_not_available = set(kwargs).intersection(
            _OPTIONS_NOT_AVAILABLE_WITH_TO_HTML
        )
        if options_not_available:
            raise TypeError(
                "These options are not available when using df.to_html: {}".format(
                    set(kwargs).intersection(options_not_available)
                )
            )
    # Default options
    for option in dir(opt):
        if (
            (not use_to_html or (option not in _OPTIONS_NOT_AVAILABLE_WITH_TO_HTML))
            and option not in kwargs
            and not option.startswith("__")
            and option not in ["read_package_file"]
        ):
            kwargs[option] = getattr(opt, option)

    for name, value in kwargs.items():
        if value is None:
            raise ValueError(
                "Please don't pass an option with a value equal to None ('{}=None')".format(
                    name
                )
            )


def to_html_datatable_using_to_html(
    df=None, caption=None, tableId=None, connected=True, import_jquery=True, **kwargs
):
    """Return the HTML representation of the given dataframe as an interactive datatable,
    using df.to_html() rather than the underlying dataframe data."""
    set_default_options(kwargs, use_to_html=True)

    # These options are used here, not in DataTable
    classes = kwargs.pop("classes")
    style = kwargs.pop("style")

    showIndex = kwargs.pop("showIndex")

    if isinstance(df, (np.ndarray, np.generic)):
        df = pd.DataFrame(df)

    if isinstance(df, (pd.Series, pl.Series)):
        df = df.to_frame()

    if showIndex == "auto":
        try:
            showIndex = df.index.name is not None or not isinstance(
                df.index, pd.RangeIndex
            )
        except AttributeError:
            # Polars DataFrame
            showIndex = False

    if "dom" not in kwargs and _df_fits_in_one_page(df, kwargs):
        kwargs["dom"] = "t"

    tableId = (
        tableId
        # default UUID in Pandas styler objects has uuid_len=5
        or str(uuid.uuid4())[:5]
    )
    if isinstance(df, pd_style.Styler):
        if not showIndex:
            try:
                df = df.hide()
            except AttributeError:
                pass

        if style:
            style = 'style="{}"'.format(style)
        else:
            style = ""

        try:
            to_html_args = dict(
                table_uuid=tableId,
                table_attributes="""class="{classes}"{style}""".format(
                    classes=classes, style=style
                ),
                caption=caption,
            )
            html_table = df.to_html(**to_html_args)
        except TypeError:
            if caption is not None:
                warnings.warn(
                    "caption is not supported by Styler.to_html in your version of Pandas"
                )
            del to_html_args["caption"]
            html_table = df.to_html(**to_html_args)
        tableId = "T_" + tableId
    else:
        if caption is not None:
            raise NotImplementedError(
                "caption is not supported when using df.to_html. "
                "Use either Pandas Style, or set use_to_html=False."
            )
        # NB: style is not available neither
        html_table = df.to_html(table_id=tableId, classes=classes)

    return html_table_from_template(
        html_table,
        table_id=tableId,
        data=None,
        kwargs=kwargs,
        connected=connected,
        import_jquery=import_jquery,
        column_filters=None,
    )


def html_table_from_template(
    html_table, table_id, data, kwargs, connected, import_jquery, column_filters
):
    css = kwargs.pop("css")
    eval_functions = kwargs.pop("eval_functions", None)
    pre_dt_code = kwargs.pop("pre_dt_code")

    # Load the HTML template
    if connected:
        output = read_package_file("html/datatables_template_connected.html")
    else:
        output = read_package_file("html/datatables_template.html")

    if not import_jquery:
        assert (
            connected
        ), "In the offline mode, jQuery is imported through init_notebook_mode"
        output = replace_value(
            output, "    import 'https://code.jquery.com/jquery-3.6.0.min.js';\n", ""
        )

    output = replace_value(
        output,
        '<table id="table_id"><thead><tr><th>A</th></tr></thead></table>',
        html_table,
    )
    output = replace_value(output, "#table_id", "#{}".format(table_id))
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
        pre_dt_code.replace("#table_id", "#{}".format(table_id)),
    )

    if data is not None:
        output = replace_value(
            output, "const data = [];", "const data = {};".format(data)
        )
    else:
        # No data since we pass the html table
        output = replace_value(output, 'dt_args["data"] = data;', "")
        output = replace_value(output, "const data = [];", "")

    return output


def _column_count_in_header(table_header):
    return max(line.count("</th>") for line in table_header.split("</tr>"))


def _min_rows(kwargs):
    if "lengthMenu" not in kwargs:
        return 10

    lengthMenu = kwargs["lengthMenu"]
    min_rows = lengthMenu[0]

    if isinstance(min_rows, (int, float)):
        return min_rows

    return min_rows[0]


def _df_fits_in_one_page(df, kwargs):
    """Display just the table (not the search box, etc...) if the rows fit on one 'page'"""
    try:
        # Pandas DF or Style
        return len(df.index) <= _min_rows(kwargs)
    except AttributeError:
        # Polars
        return len(df) <= _min_rows(kwargs)


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
    connected = kwargs.pop("connected", _CONNECTED)
    html = to_html_datatable(df, caption=caption, connected=connected, **kwargs)
    display(HTML(html))
