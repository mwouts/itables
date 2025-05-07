"""HTML/js representation of Pandas dataframes"""

import json
import re
import uuid
import warnings
from base64 import b64encode
from importlib.util import find_spec
from pathlib import Path
from typing import Any, Optional, Union, cast

import numpy as np
import pandas as pd
from typing_extensions import Unpack

from .typing import (
    DataTableOptions,
    ITableOptions,
    JavascriptCode,
    JavascriptFunction,
    check_itable_arguments,
)
from .utils import UNPKG_DT_BUNDLE_CSS_NO_VERSION, UNPKG_DT_BUNDLE_URL_NO_VERSION
from .version import __version__ as itables_version

try:
    import pandas.io.formats.style as pd_style
except ImportError:
    pd_style = None

try:
    import polars as pl
except ImportError:
    # Define pl.Series as pd.Series
    import pandas as pl

from IPython.display import HTML, display

import itables.options as opt

from .datatables_format import datatables_rows
from .downsample import downsample
from .utils import read_package_file

DATATABLES_SRC_FOR_ITABLES = (
    f"_datatables_src_for_itables_{itables_version.replace('.','_').replace('-','_')}"
)
_OPTIONS_NOT_AVAILABLE_WITH_TO_HTML = {
    "tags",
    "footer",
    "column_filters",
    "maxBytes",
    "maxRows",
    "maxColumns",
    "warn_on_unexpected_types",
}
_ORIGINAL_DATAFRAME_REPR_HTML = pd.DataFrame._repr_html_  # type: ignore
_ORIGINAL_DATAFRAME_STYLE_REPR_HTML = (
    None if pd_style is None else pd_style.Styler._repr_html_  # type: ignore
)
_ORIGINAL_POLARS_DATAFRAME_REPR_HTML = pl.DataFrame._repr_html_  # type: ignore
_CONNECTED = True
DEFAULT_LAYOUT = {
    "topStart": "pageLength",
    "topEnd": "search",
    "bottomStart": "info",
    "bottomEnd": "paging",
}
DEFAULT_LAYOUT_CONTROLS = set(DEFAULT_LAYOUT.values())


GOOGLE_COLAB = (find_spec("google") is not None) and (
    find_spec("google.colab") is not None
)


def init_notebook_mode(
    all_interactive: bool = True,
    connected: bool = GOOGLE_COLAB,
    dt_bundle: Optional[Union[Path, str]] = None,
):
    """Load the DataTables library and the corresponding css (if connected=False),
    and (if all_interactive=True), activate the DataTables representation for all the Pandas DataFrames and Series.

    Warning: make sure you keep the output of this cell when 'connected=False',
    otherwise the interactive tables will stop working.
    """
    if dt_bundle is None:
        dt_bundle = opt.dt_bundle
    global _CONNECTED
    if GOOGLE_COLAB and not connected:
        warnings.warn(
            "The offline mode for itables is not supposed to work in Google Colab. "
            "This is because HTML outputs in Google Colab are encapsulated in iframes."
        )

    _CONNECTED = connected

    if all_interactive:
        pd.DataFrame._repr_html_ = _datatables_repr_  # type: ignore
        pd.Series._repr_html_ = _datatables_repr_  # type: ignore
        if pd_style is not None:
            pd_style.Styler._repr_html_ = _datatables_repr_  # type: ignore
        pl.DataFrame._repr_html_ = _datatables_repr_  # type: ignore
        pl.Series._repr_html_ = _datatables_repr_  # type: ignore
    else:
        pd.DataFrame._repr_html_ = _ORIGINAL_DATAFRAME_REPR_HTML  # type: ignore
        if pd_style is not None:
            pd_style.Styler._repr_html_ = _ORIGINAL_DATAFRAME_STYLE_REPR_HTML  # type: ignore
        pl.DataFrame._repr_html_ = _ORIGINAL_POLARS_DATAFRAME_REPR_HTML  # type: ignore
        if hasattr(pd.Series, "_repr_html_"):
            del pd.Series._repr_html_  # type: ignore
        if hasattr(pl.Series, "_repr_html_"):
            del pl.Series._repr_html_  # type: ignore

    init_datatables = read_package_file("html/init_datatables.html")
    if not connected:
        connected_import = (
            "import { set_or_remove_dark_class } from '"
            + UNPKG_DT_BUNDLE_URL_NO_VERSION
            + "';"
        )
        local_import = (
            "const { set_or_remove_dark_class } = await import(window."
            + DATATABLES_SRC_FOR_ITABLES
            + ");"
        )
        init_datatables = replace_value(init_datatables, connected_import, local_import)
    display(HTML(init_datatables))

    if not connected:
        display(HTML(generate_init_offline_itables_html(dt_bundle)))


def get_animated_logo(display_logo_when_loading):
    if not display_logo_when_loading:
        return ""
    return f"<a href=https://mwouts.github.io/itables/>{read_package_file('logo/loading.svg')}</a>"


def generate_init_offline_itables_html(dt_bundle: Union[Path, str]) -> str:
    dt_bundle = Path(dt_bundle)
    assert dt_bundle.suffix == ".js"
    dt_src = dt_bundle.read_text(encoding="utf-8")
    dt_css = dt_bundle.with_suffix(".css").read_text(encoding="utf-8")
    dt64 = b64encode(dt_src.encode("utf-8")).decode("ascii")

    return f"""<style>{dt_css}</style>
<div style="vertical-align:middle; text-align:left">
<script>
window.{DATATABLES_SRC_FOR_ITABLES} = "data:text/javascript;base64,{dt64}";
</script>
<noscript>
{get_animated_logo(opt.display_logo_when_loading)}
This is the <code>init_notebook_mode</code> cell from ITables v{itables_version}<br>
(you should not see this message - is your notebook <it>trusted</it>?)
</noscript>
</div>
"""


def _table_header(
    df,
    table_id,
    show_index,
    classes,
    style,
    tags,
    footer,
    column_filters,
    connected,
    display_logo_when_loading,
):
    """This function returns the HTML table header. Rows are not included."""
    # Generate table head using pandas.to_html(), see issue 63
    pattern = re.compile(r".*<thead>(.*)</thead>", flags=re.MULTILINE | re.DOTALL)
    try:
        html_header = df.head(0).to_html(escape=False)
    except AttributeError:
        # Polars DataFrames
        html_header = pd.DataFrame(data=[], columns=df.columns, dtype=float).to_html()
    match = pattern.match(html_header)
    assert match is not None
    thead = match.groups()[0]
    # Don't remove the index header for empty dfs
    if not show_index and len(df.columns):
        thead = thead.replace("<th></th>", "", 1)

    itables_source = (
        "the internet" if connected else "the <code>init_notebook_mode</code> cell"
    )
    tbody = f"""<tr>
<td style="vertical-align:middle; text-align:left">
{get_animated_logo(display_logo_when_loading)}
Loading ITables v{itables_version} from {itables_source}...
(need <a href=https://mwouts.github.io/itables/troubleshooting.html>help</a>?)</td>
</tr>"""

    if style:
        style = 'style="{}"'.format(style)
    else:
        style = ""

    header = "<thead>{}</thead>".format(
        _flat_header(df, show_index) if column_filters == "header" else thead
    )

    if column_filters == "footer":
        footer = "<tfoot>{}</tfoot>".format(_flat_header(df, show_index))
    elif footer:
        footer = "<tfoot>{}</tfoot>".format(_tfoot_from_thead(thead))
    else:
        footer = ""

    return """<table id="{table_id}" class="{classes}" data-quarto-disable-processing="true" {style}>
{tags}{header}{footer}<tbody>{tbody}</tbody>
</table>""".format(
        table_id=table_id,
        classes=classes,
        style=style,
        tags=tags,
        header=header,
        tbody=tbody,
        footer=footer,
    )


def _flat_header(df, show_index):
    """When column filters are shown, we need to remove any column multiindex"""
    header = ""
    if show_index:
        for index in df.index.names:
            header += "<th>{}</th>".format(index)

    for column in df.columns:
        header += "<th>{}</th>".format(column)

    return header


def _tfoot_from_thead(thead):
    header_rows = thead.split("</tr>")
    last_row = header_rows[-1]
    assert not last_row.strip(), last_row
    header_rows = header_rows[:-1]
    return "".join(row + "</tr>" for row in header_rows[::-1] if "<tr" in row) + "\n"


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
                "One of the arguments passed to DataTable starts with 'function'. "
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


def _datatables_repr_(df):
    return to_html_datatable(df, connected=_CONNECTED)


def set_caption_from_positional_args(args: tuple, kwargs: ITableOptions):
    """Set the caption from the positional arguments"""
    if len(args):
        if len(args) != 1 or "caption" in kwargs:
            raise TypeError(
                "ITable functions or classes take at most 1 positional argument: 'caption'"
            )
        (caption,) = args
        assert isinstance(caption, str), caption
        kwargs["caption"] = caption


def to_html_datatable(
    df,
    *args,
    table_id: Optional[str] = None,
    **kwargs: Unpack[ITableOptions],
):
    """
    Return the HTML representation of the given
    dataframe as an interactive datatable
    """
    set_caption_from_positional_args(args, kwargs)
    table_id = check_table_id(table_id, kwargs)
    use_to_html = kwargs.pop("use_to_html", False)

    if "import_jquery" in kwargs:
        raise TypeError(
            "The argument 'import_jquery' was removed in ITables v2.0. "
            "Please pass a custom 'dt_url' instead."
        )

    if use_to_html or (pd_style is not None and isinstance(df, pd_style.Styler)):
        return to_html_datatable_using_to_html(
            df=df,
            table_id=table_id,
            **kwargs,
        )

    set_default_options(kwargs, use_to_html=False)

    # These options are used here, not in DataTable
    classes = kwargs.pop("classes")
    style = kwargs.pop("style")
    tags = kwargs.pop("tags")

    if "caption" in kwargs:
        tags = '{}<caption style="white-space: nowrap; overflow: hidden">{}</caption>'.format(
            tags, kwargs.pop("caption")
        )

    showIndex = kwargs.pop("showIndex")

    if isinstance(df, (np.ndarray, np.generic)):
        df = pd.DataFrame(df)  # type: ignore

    if isinstance(df, (pd.Series, pl.Series)):
        df = df.to_frame()

    if showIndex == "auto":
        if isinstance(df, pd.DataFrame):
            showIndex = df.index.name is not None or not isinstance(
                df.index, pd.RangeIndex
            )
        else:
            # Polars DataFrame
            showIndex = False

    maxBytes = kwargs.pop("maxBytes", 0)
    maxRows = kwargs.pop("maxRows", 0)
    maxColumns = kwargs.pop("maxColumns", pd.get_option("display.max_columns") or 0)
    warn_on_unexpected_types = kwargs.pop("warn_on_unexpected_types", False)

    full_row_count = len(df)
    df, downsampling_warning = downsample(
        df, max_rows=maxRows, max_columns=maxColumns, max_bytes=maxBytes
    )

    warn_on_selected_rows_not_rendered = kwargs.pop(
        "warn_on_selected_rows_not_rendered"
    )
    if "selected_rows" in kwargs:
        kwargs["selected_rows"] = warn_if_selected_rows_are_not_visible(
            kwargs["selected_rows"],
            full_row_count,
            len(df),
            warn_on_selected_rows_not_rendered,
        )

    if downsampling_warning:
        kwargs["downsampling_warning"] = downsampling_warning
    kwargs["filtered_row_count"] = full_row_count - len(df)

    _adjust_layout(
        df,
        kwargs,
        downsampling_warning=downsampling_warning,
        warn_on_dom=kwargs.pop("warn_on_dom"),
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

    table_id = table_id or "itables_" + str(uuid.uuid4()).replace("-", "_")
    if isinstance(classes, list):
        classes = " ".join(classes)

    if not showIndex:
        if isinstance(df, pd.DataFrame):
            df = df.set_index(pd.RangeIndex(len(df.index)))

    table_header = _table_header(
        df,
        table_id,
        showIndex,
        classes,
        style,
        tags,
        footer,
        column_filters,
        connected=kwargs.get("connected"),
        display_logo_when_loading=kwargs.pop("display_logo_when_loading"),
    )

    # Export the table data to JSON and include this in the HTML
    if showIndex:
        df = safe_reset_index(df)

    # When the header has an extra column, we add
    # an extra empty column in the table data #141
    column_count = _column_count_in_header(table_header)
    data_json = datatables_rows(
        df,
        column_count,
        warn_on_unexpected_types=warn_on_unexpected_types,
    )

    return html_table_from_template(
        table_header,
        table_id=table_id,
        data_json=data_json,
        kwargs=kwargs,
        column_filters=column_filters,
    )


def _raise_if_javascript_code(values, context=""):
    if isinstance(values, (JavascriptCode, JavascriptFunction)):
        raise TypeError(f"Javascript code can't be passed to the extension: {context}")

    if isinstance(values, dict):
        for key, value in values.items():
            _raise_if_javascript_code(value, f"{context}/{key}")
        return

    if isinstance(values, list):
        for i, value in enumerate(values):
            _raise_if_javascript_code(value, f"{context}/{i}")
        return


def get_itables_extension_arguments(df, *args, **kwargs: Unpack[ITableOptions]):
    """
    This function returns two dictionaries that are JSON
    serializable and can be passed to the itables extensions.
    The first dict contains the arguments to be passed to the
    DataTable constructor, while the second one contains other
    parameters to be used outside of the constructor.
    """
    # Pandas style objects are not supported
    if pd_style is not None and isinstance(df, pd_style.Styler):
        raise NotImplementedError(
            "Pandas style objects can't be used with the extension"
        )

    set_caption_from_positional_args(args, kwargs)

    if df is None:
        df = pd.DataFrame()

    set_default_options(
        kwargs,
        use_to_html=False,
        context="Python apps",
        not_available=[
            "columns",
            "tags",
            "dt_url",
            "connected",
            "pre_dt_code",
            "use_to_html",
            "footer",
            "column_filters",
            "display_logo_when_loading",
        ],
    )

    # Javascript code is not supported in the extension
    _raise_if_javascript_code(kwargs)

    # These options are used here, not in DataTable
    classes = kwargs.pop("classes")
    style = kwargs.pop("style")
    showIndex = kwargs.pop("showIndex")

    if isinstance(df, (np.ndarray, np.generic)):
        df = pd.DataFrame(df)  # type: ignore

    if isinstance(df, (pd.Series, pl.Series)):
        df = df.to_frame()  # type: ignore

    if showIndex == "auto":
        if isinstance(df, pd.DataFrame):
            showIndex = df.index.name is not None or not isinstance(
                df.index, pd.RangeIndex
            )
        else:
            # Polars DataFrame
            showIndex = False

    maxBytes = kwargs.pop("maxBytes", 0)
    maxRows = kwargs.pop("maxRows", 0)
    maxColumns = kwargs.pop("maxColumns", pd.get_option("display.max_columns") or 0)
    warn_on_unexpected_types = kwargs.pop("warn_on_unexpected_types", False)

    full_row_count = len(df)
    df, downsampling_warning = downsample(
        df, max_rows=maxRows, max_columns=maxColumns, max_bytes=maxBytes
    )

    _adjust_layout(
        df,
        kwargs,
        downsampling_warning=downsampling_warning,
        warn_on_dom=kwargs.pop("warn_on_dom"),
    )

    if isinstance(classes, list):
        classes = " ".join(classes)

    if not showIndex:
        if isinstance(df, pd.DataFrame):
            df = df.set_index(pd.RangeIndex(len(df.index)))

    if showIndex:
        df = safe_reset_index(df)

    if isinstance(df.columns, pd.MultiIndex):
        columns = [
            {"title": "<br>".join(str(level) or "&nbsp" for level in col)}
            for col in df.columns
        ]
    else:
        columns = [{"title": str(col)} for col in df.columns]

    data_json = ""
    try:
        data_json = datatables_rows(df, None, warn_on_unexpected_types)
    except ValueError as e:
        raise NotImplementedError(
            f"This dataframe can't be serialized to JSON:\n{e}\n{df}"
        )

    try:
        data = json.loads(data_json)
    except (ValueError, json.JSONDecodeError) as e:
        raise NotImplementedError(
            f"This dataframe can't be serialized to JSON:\n{e}\n{data_json}"
        )

    assert len(data) <= full_row_count

    selected_rows = warn_if_selected_rows_are_not_visible(
        kwargs.pop("selected_rows", None),
        full_row_count,
        len(data),
        kwargs.pop("warn_on_selected_rows_not_rendered"),
    )

    check_itable_arguments(cast(dict[str, Any], kwargs), DataTableOptions)

    other_args = {
        "classes": classes,
        "style": style,
        "caption": kwargs.pop("caption", None),
    }
    dt_args = {
        "columns": columns,
        "data_json": data_json,
        "filtered_row_count": full_row_count - len(data),
        **kwargs,
    }
    if downsampling_warning:
        dt_args["downsampling_warning"] = downsampling_warning
    if selected_rows is not None:
        other_args["selected_rows"] = selected_rows
    return dt_args, other_args


def warn_if_selected_rows_are_not_visible(
    selected_rows, full_row_count, data_row_count, warn_on_selected_rows_not_rendered
):
    if selected_rows is None:
        return []

    if not all(isinstance(i, int) for i in selected_rows):
        raise TypeError("Selected rows must be integers")

    if selected_rows and (
        min(selected_rows) < 0 or max(selected_rows) >= full_row_count
    ):
        raise IndexError("Selected rows out of range")

    if full_row_count == data_row_count:
        return selected_rows

    second_half = data_row_count // 2
    first_half = data_row_count - second_half
    assert first_half >= second_half

    bottom_limit = first_half
    top_limit = full_row_count - second_half

    if warn_on_selected_rows_not_rendered and any(
        bottom_limit <= i < top_limit for i in selected_rows
    ):
        not_shown = [i for i in selected_rows if bottom_limit <= i < top_limit]
        not_shown = ", ".join(
            [str(i) for i in not_shown[:6]] + (["..."] if len(not_shown) > 6 else [])
        )
        warnings.warn(
            f"This table has been downsampled, see https://mwouts.github.io/itables/downsampling.html. "
            f"Only {data_row_count} of the original {full_row_count} rows are rendered. "
            f"In particular these rows: [{not_shown}] cannot be selected "
            f"(more generally, no row with index between {bottom_limit} and {top_limit-1} "
            "can be selected). Hint: increase maxBytes if appropriate - see link above."
        )

    return [i for i in selected_rows if i < bottom_limit or i >= top_limit]


def check_table_id(table_id: Optional[str], kwargs: DataTableOptions) -> Optional[str]:
    """Make sure that the table_id is a valid HTML id.

    See also https://stackoverflow.com/questions/70579/html-valid-id-attribute-values
    """
    if "tableId" in kwargs:
        warnings.warn(
            "tableId has been deprecated, please use table_id instead",
            DeprecationWarning,
        )
        assert table_id is None
        table_id = kwargs.pop("tableId")

    if table_id is not None:
        if not re.match(r"[A-Za-z][-A-Za-z0-9_.]*", table_id):
            raise ValueError(
                "The id name must contain at least one character, "
                f"cannot start with a number, and must not contain whitespaces ({table_id})"
            )

    return table_id


def set_default_options(kwargs, use_to_html, context=None, not_available=()):
    if "connected" not in not_available:
        kwargs["connected"] = kwargs.get(
            "connected", ("dt_url" in kwargs) or _CONNECTED
        )
    args_not_available = set(kwargs).intersection(not_available)
    if args_not_available:
        raise TypeError(
            f"In {context}, " f"these options are not available: {args_not_available}"
        )
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

    # layout is updated using the arguments passed on to show
    kwargs["layout"] = {**getattr(opt, "layout"), **kwargs.get("layout", {})}

    # Default options
    for option in dir(opt):
        if (
            option not in not_available
            and (not use_to_html or (option not in _OPTIONS_NOT_AVAILABLE_WITH_TO_HTML))
            and option not in kwargs
            and not option.startswith("_")
            and option
            not in {
                # this one is for init_notebook_mode
                "dt_bundle"
            }
        ):
            kwargs[option] = getattr(opt, option)

    if kwargs.get("scrollX", False):
        # column headers are misaligned if we have margin:auto
        kwargs["style"] = kwargs["style"].replace("margin:auto", "margin:0")

    for name, value in kwargs.items():
        if value is None:
            raise ValueError(
                "Please don't pass an option with a value equal to None ('{}=None')".format(
                    name
                )
            )

    dt_args = set(ITableOptions.__optional_keys__) - set(
        DataTableOptions.__optional_keys__
    )
    check_itable_arguments(
        {k: v for k, v in kwargs.items() if k not in dt_args}, ITableOptions
    )


def to_html_datatable_using_to_html(
    df, *args, table_id: Optional[str] = None, **kwargs: Unpack[ITableOptions]
):
    """Return the HTML representation of the given dataframe as an interactive datatable,
    using df.to_html() rather than the underlying dataframe data."""
    set_caption_from_positional_args(args, kwargs)
    table_id = check_table_id(table_id, kwargs)
    set_default_options(
        kwargs,
        use_to_html=True,
        not_available=(
            "warn_on_selected_rows_not_rendered",
            "display_logo_when_loading",
        ),
    )

    # These options are used here, not in DataTable
    classes = kwargs.pop("classes")
    style = kwargs.pop("style")

    showIndex = kwargs.pop("showIndex")

    if isinstance(df, (np.ndarray, np.generic)):
        df = pd.DataFrame(df)  # type: ignore[assignment]

    if isinstance(df, (pd.Series, pl.Series)):
        df = df.to_frame()

    if showIndex == "auto":
        if isinstance(df, pd.DataFrame):
            showIndex = df.index.name is not None or not isinstance(
                df.index, pd.RangeIndex
            )
        else:
            # Polars DataFrame
            showIndex = False

    _adjust_layout(
        df, kwargs, downsampling_warning="", warn_on_dom=kwargs.pop("warn_on_dom")
    )

    table_id = (
        table_id
        # default UUID in Pandas styler objects has uuid_len=5
        or str(uuid.uuid4())[:5]
    )
    if pd_style is not None and isinstance(df, pd_style.Styler):
        if not showIndex:
            try:
                df = df.hide()
            except AttributeError:
                pass

        if style:
            style = 'style="{}"'.format(style)
        else:
            style = ""

        table_attributes = """class="{classes}"{style}""".format(
            classes=classes, style=style
        )

        try:
            html_table = df.to_html(
                table_uuid=table_id,
                table_attributes=table_attributes,
                caption=kwargs.get("caption"),
                sparse_index=False,
            )
        except TypeError:
            if "caption" in kwargs:
                warnings.warn(
                    "caption is not supported by Styler.to_html in your version of Pandas"
                )
            html_table = df.to_html(
                table_uuid=table_id, table_attributes=table_attributes
            )
        table_id = "T_" + table_id
    else:
        if "caption" in kwargs:
            raise NotImplementedError(
                "caption is not supported when using df.to_html. "
                "Use either Pandas Style, or set use_to_html=False."
            )
        # NB: style is not available either
        html_table = df.to_html(table_id=table_id, classes=classes)  # type: ignore

    return html_table_from_template(
        html_table,
        table_id=table_id,
        data_json=None,
        kwargs=kwargs,
        column_filters=None,
    )


def html_table_from_template(html_table, table_id, data_json, kwargs, column_filters):
    if "css" in kwargs:
        TypeError(
            "The 'css' argument has been deprecated, see the new "
            "approach at https://mwouts.github.io/itables/custom_css.html."
        )
    eval_functions = kwargs.pop("eval_functions", None)
    pre_dt_code = kwargs.pop("pre_dt_code")
    dt_url = kwargs.pop("dt_url")

    # Load the HTML template
    output = read_package_file("html/datatables_template.html")
    if kwargs.pop("connected"):
        assert dt_url.endswith(".js")
        output = replace_value(output, UNPKG_DT_BUNDLE_URL_NO_VERSION, dt_url)
        output = replace_value(
            output,
            UNPKG_DT_BUNDLE_CSS_NO_VERSION,
            dt_url[:-3] + ".css",
        )
    else:
        connected_style = (
            f'<link href="{UNPKG_DT_BUNDLE_CSS_NO_VERSION}" rel="stylesheet">\n'
        )
        output = replace_value(output, connected_style, "")
        connected_import = (
            "import { ITable, jQuery as $ } from '"
            + UNPKG_DT_BUNDLE_URL_NO_VERSION
            + "';"
        )
        local_import = (
            "const { ITable, jQuery: $ } = await import(window."
            + DATATABLES_SRC_FOR_ITABLES
            + ");"
        )
        output = replace_value(output, connected_import, local_import)

    output = replace_value(
        output,
        '<table id="table_id"><thead><tr><th>A</th></tr></thead></table>',
        html_table,
    )
    output = replace_value(output, "#table_id", "#{}".format(table_id))

    if "selected_rows" in kwargs:
        output = replace_value(
            output,
            "new ITable(table, dt_args);",
            f"""let dt = new ITable(table, dt_args);
        dt.selected_rows = {kwargs.pop("selected_rows")};
""",
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
    check_itable_arguments(kwargs, DataTableOptions)
    if data_json is not None:
        kwargs["data_json"] = data_json
    dt_args = json_dumps(kwargs, eval_functions)

    output = replace_value(
        output, "let dt_args = {};", "let dt_args = {};".format(dt_args)
    )
    output = replace_value(
        output,
        "// [pre-dt-code]",
        pre_dt_code.replace("#table_id", "#{}".format(table_id)),
    )

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


def _adjust_layout(df, kwargs, *, downsampling_warning, warn_on_dom):
    has_default_layout = kwargs["layout"] == DEFAULT_LAYOUT

    if "dom" in kwargs:
        if warn_on_dom:
            warnings.warn(
                "The 'dom' argument has been deprecated in DataTables==2.0.",
                DeprecationWarning,
            )
        if not has_default_layout:
            raise ValueError("You cannot pass both 'dom' and 'layout'")
        del kwargs["layout"]
        has_default_layout = False

    if has_default_layout and _df_fits_in_one_page(df, kwargs):
        kwargs["layout"] = {
            key: _filter_control(control, downsampling_warning)
            for key, control in kwargs["layout"].items()
        }

    if (
        "buttons" in kwargs
        and "layout" in kwargs
        and "buttons" not in kwargs["layout"].values()
    ):
        kwargs["layout"] = {**kwargs["layout"], "topStart": "buttons"}


def _df_fits_in_one_page(df, kwargs):
    """Display just the table (not the search box, etc...) if the rows fit on one 'page'"""
    try:
        # Pandas DF or Style
        return len(df.index) <= _min_rows(kwargs)
    except AttributeError:
        # Polars
        return len(df) <= _min_rows(kwargs)


def _filter_control(control, downsampling_warning):
    if control == "info" and downsampling_warning:
        return control
    if control not in DEFAULT_LAYOUT_CONTROLS:
        return control
    return None


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


def show(df=None, *args, **kwargs: Unpack[ITableOptions]):
    """Render the given dataframe as an interactive datatable"""
    display(HTML(to_html_datatable(df, *args, **kwargs)))
