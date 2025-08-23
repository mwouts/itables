"""HTML/js representation of Pandas dataframes"""

import json
import re
import uuid
import warnings
from base64 import b64encode
from importlib.util import find_spec
from pathlib import Path
from typing import (
    Any,
    Mapping,
    Optional,
    Sequence,
    Union,
    cast,
)

import numpy as np
import pandas as pd
from typing_extensions import Unpack

from .typing import (
    DataFrameOrSeries,
    DTForITablesOptions,
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
_OPTIONS_NOT_AVAILABLE_IN_APP_MODE = {
    "connected",
    "dt_url",
    "display_logo_when_loading",
}
_OPTIONS_NOT_AVAILABLE_WITH_TO_HTML = {
    "footer",
    "column_filters",
    "maxBytes",
    "maxRows",
    "maxColumns",
    "warn_on_unexpected_types",
    "warn_on_selected_rows_not_rendered",
    "display_logo_when_loading",
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


def get_compact_classes(classes: Union[str, Sequence[str]]) -> str:
    """Convert a list of classes to a compact string"""
    if isinstance(classes, str):
        return classes
    elif isinstance(classes, list):
        return " ".join(classes)
    else:
        raise TypeError(f"classes must be a string or a list, not {type(classes)}")


def get_expanded_classes(classes: Union[str, Sequence[str]]) -> Sequence[str]:
    """Convert a class string to a list"""
    if isinstance(classes, str):
        return classes.split()
    elif isinstance(classes, list):
        return classes
    else:
        raise TypeError(f"classes must be a string or a list, not {type(classes)}")


def get_compact_style(style: Union[str, Mapping[str, str]]) -> str:
    """Convert a style to a compact string"""
    if isinstance(style, str):
        return style
    elif isinstance(style, Mapping):
        return ";".join(f"{k}:{v}" for k, v in style.items())
    else:
        raise TypeError(f"style must be a string or a dict, not {type(style)}")


def get_expanded_style(style: Union[str, Mapping[str, str]]) -> dict[str, str]:
    """Convert a style to a dict"""
    if isinstance(style, Mapping):
        return dict(**style)
    elif isinstance(style, str):
        return {
            k.strip(): v.strip()
            for k, v in (item.split(":") for item in style.split(";") if item.strip())
        }
    else:
        raise TypeError(f"style must be a string or a dict, not {type(style)}")


def init_notebook_mode(
    all_interactive: bool = True,
    connected: bool = GOOGLE_COLAB,
    dt_bundle: Optional[Union[Path, str]] = None,
) -> None:
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


def get_animated_logo(display_logo_when_loading: bool) -> str:
    """Return the HTML for the loading logo of ITables"""
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
    show_index,
    footer,
    column_filters,
    escape_html: bool,
):
    """This function returns the HTML table header. Rows are not included."""
    # Generate table head using pandas.to_html(), see issue 63
    pattern = re.compile(r".*<thead>(.*)</thead>", flags=re.MULTILINE | re.DOTALL)
    try:
        html_header = df.head(0).to_html(escape=escape_html)
    except AttributeError:
        # Polars DataFrames
        html_header = pd.DataFrame(data=[], columns=df.columns, dtype=float).to_html()
    match = pattern.match(html_header)
    assert match is not None
    thead = match.groups()[0]
    # Don't remove the index header for empty dfs
    if not show_index and len(df.columns):
        thead = thead.replace("<th></th>", "", 1)

    header = "<thead>{}</thead>".format(
        _flat_header(df, show_index) if column_filters == "header" else thead
    )

    if column_filters == "footer":
        footer = "<tfoot>{}</tfoot>".format(_flat_header(df, show_index))
    elif footer:
        footer = "<tfoot>{}</tfoot>".format(_tfoot_from_thead(thead))
    else:
        footer = ""

    return f"<table>{header}{footer}</table>"


def _flat_header(df, show_index):
    """When column filters are shown, we need to remove any column multiindex"""
    header = ""
    if show_index:
        for index in df.index.names:
            header += "<th>{}</th>".format(index)

    for column in df.columns:
        header += "<th>{}</th>".format(column)

    return header


def _tfoot_from_thead(thead: str) -> str:
    header_rows = thead.split("</tr>")
    last_row = header_rows[-1]
    assert not last_row.strip(), last_row
    header_rows = header_rows[:-1]
    return "".join(row + "</tr>" for row in header_rows[::-1] if "<tr" in row) + "\n"


def get_keys_to_be_evaluated(data: Any) -> list[list[Union[int, str]]]:
    """
    This function returns the keys that need to be evaluated
    in the ITable arguments
    """
    if isinstance(data, str):
        return []
    keys_to_be_evaluated = []
    if isinstance(data, Sequence):
        data = dict(enumerate(data))
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, (JavascriptCode, JavascriptFunction)):
                keys_to_be_evaluated.append([key])
            else:
                nested_keys = get_keys_to_be_evaluated(value)
                if nested_keys:
                    for nested_key in nested_keys:
                        keys_to_be_evaluated.append([key] + nested_key)

    return keys_to_be_evaluated


def replace_value(template: str, pattern: str, value: str) -> str:
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


def _datatables_repr_(df: DataFrameOrSeries) -> str:
    return to_html_datatable(df, connected=_CONNECTED)


def to_html_datatable(
    df: DataFrameOrSeries,
    caption: Optional[str] = None,
    **kwargs: Unpack[ITableOptions],
) -> str:
    """
    Return the HTML representation of the given
    dataframe as an interactive datatable
    """
    kwargs["table_id"] = table_id = check_table_id(
        kwargs.pop("table_id", None), kwargs, df=df
    )
    dt_args = get_itable_arguments(df, caption, **kwargs)
    dt_url = dt_args.pop("dt_url")
    connected = dt_args.pop("connected")
    display_logo_when_loading = dt_args.pop("display_logo_when_loading", False)

    check_itable_arguments(cast(dict[str, Any], dt_args), DTForITablesOptions)
    return html_table_from_template(
        table_id=table_id,
        dt_url=dt_url,
        connected=connected,
        display_logo_when_loading=display_logo_when_loading,
        kwargs=dt_args,
    )


def _evaluate_show_index(df, showIndex) -> bool:
    """
    We don't want to show trivial indices (RangeIndex with no name) on Pandas DataFrames.
    """
    if df is None:
        return False
    if pl is not pd and isinstance(df, pl.DataFrame):
        return False
    if showIndex != "auto":
        return showIndex
    if isinstance(df, pd.DataFrame):
        return df.index.name is not None or not isinstance(df.index, pd.RangeIndex)
    if pd_style is not None and isinstance(df, pd_style.Styler):
        return _evaluate_show_index(
            df.data,  # pyright: ignore[reportAttributeAccessIssue]
            showIndex,
        )
    raise NotImplementedError(type(df))


def get_itable_arguments(
    df: DataFrameOrSeries,
    caption: Optional[str] = None,
    app_mode: bool = False,
    **kwargs: Unpack[ITableOptions],
) -> DTForITablesOptions:
    """
    Return the arguments to be passed to the ITable class
    """
    if "import_jquery" in kwargs:
        raise TypeError(
            "The argument 'import_jquery' was removed in ITables v2.0. "
            "Please pass a custom 'dt_url' instead."
        )

    if pd_style is not None and isinstance(df, pd_style.Styler):
        use_to_html = kwargs.pop("use_to_html", True)
        if not use_to_html:
            raise ValueError("We have to use df.to_html() for Pandas Styler objects")
    else:
        use_to_html = kwargs.pop("use_to_html", False)

    set_default_options(kwargs, use_to_html=use_to_html, app_mode=app_mode)

    showIndex = kwargs.pop("showIndex")

    if isinstance(df, (np.ndarray, np.generic)):
        df = pd.DataFrame(df)  # type: ignore

    if isinstance(df, (pd.Series, pl.Series)):
        df = df.to_frame()

    showIndex = _evaluate_show_index(df, showIndex)

    maxBytes = kwargs.pop("maxBytes", 0)
    maxRows = kwargs.pop("maxRows", 0)
    maxColumns = kwargs.pop("maxColumns", pd.get_option("display.max_columns") or 0)
    warn_on_unexpected_types = kwargs.pop("warn_on_unexpected_types", False)
    allow_html = kwargs.pop("allow_html")

    if not showIndex:
        if isinstance(df, pd.DataFrame):
            df = df.set_index(pd.RangeIndex(len(df.index)))

    table_id = kwargs.pop("table_id", None)
    footer = kwargs.pop("footer", False)
    warn_on_selected_rows_not_rendered = kwargs.pop(
        "warn_on_selected_rows_not_rendered", False
    )
    dt_args = cast(DTForITablesOptions, kwargs)
    if caption is not None:
        dt_args["caption"] = caption
    del kwargs

    if df is None:
        pass
    elif not use_to_html:
        full_row_count = len(df)  # type: ignore
        df, downsampling_warning = downsample(
            df, max_rows=maxRows, max_columns=maxColumns, max_bytes=maxBytes
        )

        if "selected_rows" in dt_args:
            dt_args["selected_rows"] = warn_if_selected_rows_are_not_visible(
                dt_args["selected_rows"],
                full_row_count,
                len(df),
                warn_on_selected_rows_not_rendered,
            )

        if downsampling_warning:
            dt_args["downsampling_warning"] = downsampling_warning
            dt_args["filtered_row_count"] = full_row_count - len(df)

        if dt_args.get("column_filters", False) == "footer":
            footer = True

        table_header = _table_header(
            df,
            showIndex,
            footer,
            dt_args.get("column_filters", False),
            escape_html=allow_html is not True,
        )

        # Export the table data to JSON and include this in the HTML
        if showIndex:
            df = safe_reset_index(df)

        # When the header has an extra column, we add
        # an extra empty column in the table data #141
        column_count = _column_count_in_header(table_header)
        dt_args["table_html"] = table_header
        dt_args["data_json"] = datatables_rows(
            df,
            column_count,
            warn_on_unexpected_types=warn_on_unexpected_types,
            escape_html=allow_html is not True,
        )
    else:
        if pd_style is not None and isinstance(df, pd_style.Styler):
            if not allow_html:
                raise ValueError(
                    "Pandas Styler objects always use HTML. Please make sure that you trust the "
                    "content of that table. If so, please render it with allow_html=True, cf. "
                    "https://mwouts.github.io/itables/options/allow_html.html."
                )
            if not showIndex:
                try:
                    df = df.hide()
                except AttributeError:
                    pass

            assert isinstance(table_id, str)
            assert table_id.startswith("T_")
            table_id = table_id[2:]
            assert isinstance(df, pd_style.Styler)
            try:
                table_html = df.to_html(sparse_index=False, table_uuid=table_id)
            except TypeError:
                table_html = df.to_html(table_uuid=table_id)

            # We need to extract the style from the table
            table_style, table_html = table_html.split("</style>", 1)
            style_prefix = '<style type="text/css">'
            assert table_style.startswith(style_prefix)
            dt_args["table_style"] = table_style.removeprefix(style_prefix)
            dt_args["table_html"] = table_html
        else:
            # NB: style is not available either
            dt_args["table_html"] = df.to_html(escape=allow_html is not True)  # type: ignore

    _adjust_layout(df, dt_args)

    if dt_args.get("column_filters") is False:
        dt_args.pop("column_filters")
    if dt_args.get("text_in_header_can_be_selected") is False:
        dt_args.pop("text_in_header_can_be_selected")

    keys_to_be_evaluated = get_keys_to_be_evaluated(dt_args)
    if keys_to_be_evaluated:
        dt_args["keys_to_be_evaluated"] = keys_to_be_evaluated

    return dt_args


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


def get_itables_extension_arguments(
    df: Optional[DataFrameOrSeries],
    caption: Optional[str] = None,
    **kwargs: Unpack[ITableOptions],
) -> tuple[DTForITablesOptions, dict[str, Any]]:
    """
    This function returns two dictionaries that are JSON
    serializable and can be passed to the ITable extensions.
    The first dict contains the arguments to be passed to the
    DataTable constructor, while the second one contains other
    parameters to be used outside of the constructor.
    """
    kwargs["table_id"] = check_table_id(kwargs.get("table_id", None), kwargs, df=df)
    dt_args = get_itable_arguments(df, caption, **kwargs, app_mode=True)
    check_itable_arguments(cast(dict[str, Any], dt_args), DTForITablesOptions)
    other_args = {
        "classes": get_compact_classes(dt_args.pop("classes")),
        "style": get_compact_style(dt_args.pop("style")),
        "caption": dt_args.pop("caption", None),
        "selected_rows": dt_args.pop("selected_rows", []),
    }
    return dt_args, other_args


def warn_if_selected_rows_are_not_visible(
    selected_rows: Optional[Sequence[int]],
    full_row_count: int,
    data_row_count: int,
    warn_on_selected_rows_not_rendered: bool,
) -> Sequence[int]:
    """
    Issue a warning if the selected rows are not within the range of rendered rows.
    """
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


def check_table_id(
    table_id: Optional[str],
    kwargs: Union[ITableOptions, DTForITablesOptions],
    df: Optional[DataFrameOrSeries] = None,
) -> str:
    """Make sure that the table_id is a valid HTML id.

    See also https://stackoverflow.com/questions/70579/html-valid-id-attribute-values
    """
    if "tableId" in kwargs:
        raise TypeError(
            "tableId has been deprecated, please use table_id instead",
        )

    if table_id is None:
        if pd_style is not None and isinstance(df, pd_style.Styler):
            return "T_" + str(uuid.uuid4())[:5]

        return "itables_" + str(uuid.uuid4()).replace("-", "_")

    if not re.match(r"[A-Za-z][-A-Za-z0-9_.]*", table_id):
        raise ValueError(
            "The id name must contain at least one character, "
            f"cannot start with a number, and must not contain whitespaces ({table_id})"
        )

    return table_id


def set_default_options(
    kwargs: ITableOptions, *, use_to_html: bool, app_mode: bool
) -> None:
    if not app_mode:
        kwargs["connected"] = kwargs.get(
            "connected", ("dt_url" in kwargs) or _CONNECTED
        )
    not_available = {"dt_bundle"}  # this one is for init_notebook_mode
    if use_to_html:
        not_available = not_available.union(_OPTIONS_NOT_AVAILABLE_WITH_TO_HTML)
    if app_mode:
        not_available = not_available.union(_OPTIONS_NOT_AVAILABLE_IN_APP_MODE)

    options_not_available = set(kwargs).intersection(not_available)
    if options_not_available:
        raise TypeError(
            f"These options are not available with {use_to_html=} {app_mode=}: "
            f"{set(kwargs).intersection(options_not_available)}"
        )

    # layout is updated using the arguments passed on to show
    kwargs["layout"] = {**getattr(opt, "layout"), **kwargs.get("layout", {})}

    # Default options
    for option in (
        set(dir(opt))
        .difference(opt.__non_options)
        .difference(not_available)
        .difference(kwargs)
    ):
        kwargs[option] = getattr(opt, option)

    if "classes" in kwargs and isinstance(kwargs["classes"], list):
        kwargs["classes"] = " ".join(kwargs["classes"])

    if "style" in kwargs and isinstance(kwargs["style"], dict):
        kwargs["style"] = ";".join(f"{k}:{v}" for k, v in kwargs["style"].items())

    if kwargs.get("scrollX", False):
        # column headers are misaligned if we have margin:auto
        assert "style" in kwargs
        assert isinstance(kwargs["style"], str)
        kwargs["style"] = kwargs["style"].replace("margin:auto", "margin:0")

    for name, value in kwargs.items():
        if value is None:
            raise ValueError(
                "Please don't pass an option with a value equal to None ('{}=None')".format(
                    name
                )
            )

    # The options for ITable in dt_for_itables will be checked later on
    check_itable_arguments(
        {
            k: v
            for k, v in kwargs.items()
            if k not in DTForITablesOptions.__optional_keys__
        },
        ITableOptions,
    )


def html_table_from_template(
    table_id: str,
    dt_url: str,
    connected: bool,
    display_logo_when_loading: bool,
    kwargs: DTForITablesOptions,
) -> str:
    if "css" in kwargs:
        raise TypeError(
            "The 'css' argument has been deprecated, see the new "
            "approach at https://mwouts.github.io/itables/css.html."
        )

    # Load the HTML template
    output = read_package_file("html/datatables_template.html")
    if connected:
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

    itables_source = (
        "the internet" if connected else "the <code>init_notebook_mode</code> cell"
    )
    table_body = f"""<tbody><tr>
    <td style="vertical-align:middle; text-align:left">
    {get_animated_logo(display_logo_when_loading)}
    Loading ITables v{itables_version} from {itables_source}...
    (need <a href=https://mwouts.github.io/itables/troubleshooting.html>help</a>?)</td>
    </tr></tbody>"""
    check_table_id(table_id, kwargs)
    output = replace_value(
        output,
        '<table id="table_id"></table>',
        f'<table id="{table_id}">{table_body}</table>',
    )
    output = replace_value(output, "#table_id", f"#{table_id}")

    assert "classes" in kwargs
    kwargs["classes"] = get_expanded_classes(kwargs["classes"])
    assert "style" in kwargs
    kwargs["style"] = get_expanded_style(kwargs["style"])

    # Export the DT args to JSON
    dt_args = json.dumps(kwargs)
    output = replace_value(
        output, "let dt_args = {};", "let dt_args = {};".format(dt_args)
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


def _adjust_layout(df, kwargs):
    has_default_layout = kwargs["layout"] == DEFAULT_LAYOUT

    if has_default_layout and _df_fits_in_one_page(df, kwargs):
        kwargs["layout"] = {
            key: _filter_control(control, kwargs.get("downsampling_warning", ""))
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
    if df is None:
        return True
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


def safe_reset_index(df: pd.DataFrame) -> pd.DataFrame:
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


def show(
    df: DataFrameOrSeries,
    caption: Optional[str] = None,
    **kwargs: Unpack[ITableOptions],
) -> None:
    """Render the given dataframe as an interactive datatable"""
    display(HTML(to_html_datatable(df, caption, **kwargs)))
