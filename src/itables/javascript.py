"""HTML/js representation of Pandas dataframes"""

import json
import re
import sys
import uuid
import warnings
from base64 import b64encode
from importlib.util import find_spec
from pathlib import Path
from typing import Any, Literal, Mapping, Optional, Sequence, Union, cast

import itables.options as opt

from .datatables_format import datatables_rows, escape_html_chars
from .downsample import downsample
from .typing import (
    DataFrameModuleName,
    DataFrameOrSeries,
    DTForITablesOptions,
    ITableOptions,
    JavascriptCode,
    JavascriptFunction,
    Unpack,
    check_itable_arguments,
    get_dataframe_module_and_type_name,
    get_dataframe_type_description,
)
from .utils import (
    UNPKG_DT_BUNDLE_CSS_NO_VERSION,
    UNPKG_DT_BUNDLE_URL_NO_VERSION,
    read_package_file,
)
from .version import __version__ as itables_version

_ITABLES_UNDERSCORE_VERSION = (
    f"_itables_{itables_version.replace('.','_').replace('-','_')}"
)
_ITABLES_READY_EVENT = f"itables-{itables_version}-ready"
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
_ORIGINAL_REPR_HTML = {}
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


def set_itables_repr_html_methods(all_interactive: bool) -> None:
    """Set the _repr_html_ methods according to all_interactive, after saving the original ones"""
    global _ORIGINAL_REPR_HTML
    try:
        import pandas as pd
    except ImportError:
        pass
    else:
        if "pd.DataFrame" not in _ORIGINAL_REPR_HTML:
            _ORIGINAL_REPR_HTML["pd.DataFrame"] = pd.DataFrame._repr_html_  # type: ignore

        if all_interactive:
            pd.DataFrame._repr_html_ = _datatables_repr_  # type: ignore
            pd.Series._repr_html_ = _datatables_repr_  # type: ignore
        else:
            pd.DataFrame._repr_html_ = _ORIGINAL_REPR_HTML["pd.DataFrame"]  # type: ignore
            if hasattr(pd.Series, "_repr_html_"):
                del pd.Series._repr_html_  # type: ignore

    try:
        import pandas.io.formats.style as pd_style  # type: ignore
    except ImportError:
        pass
    else:
        if "pd.Styler" not in _ORIGINAL_REPR_HTML:
            _ORIGINAL_REPR_HTML["pd.Styler"] = pd_style.Styler._repr_html_  # type: ignore

        if all_interactive:
            pd_style.Styler._repr_html_ = _datatables_repr_  # type: ignore
        else:
            pd_style.Styler._repr_html_ = _ORIGINAL_REPR_HTML["pd.Styler"]  # type: ignore

    try:
        import polars as pl
    except ImportError:
        pass
    else:
        if "pl.DataFrame" not in _ORIGINAL_REPR_HTML:
            _ORIGINAL_REPR_HTML["pl.DataFrame"] = pl.DataFrame._repr_html_  # type: ignore

        if all_interactive:
            pl.DataFrame._repr_html_ = _datatables_repr_  # type: ignore
            pl.Series._repr_html_ = _datatables_repr_  # type: ignore
        else:
            pl.DataFrame._repr_html_ = _ORIGINAL_REPR_HTML["pl.DataFrame"]  # type: ignore
            if hasattr(pl.Series, "_repr_html_"):
                del pl.Series._repr_html_  # type: ignore


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

    set_itables_repr_html_methods(all_interactive)

    init_datatables = read_package_file("html/init_datatables.html")
    if not connected:
        connected_import = (
            "import { set_or_remove_dark_class } from '"
            + UNPKG_DT_BUNDLE_URL_NO_VERSION
            + "';"
        )
        local_import = (
            "const { set_or_remove_dark_class } = await window."
            + _ITABLES_UNDERSCORE_VERSION
            + ";"
        )
        init_datatables = replace_value(init_datatables, connected_import, local_import)

    from IPython.display import HTML, display

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
    dt_src_b64 = b64encode(dt_src.encode("utf-8")).decode("ascii")
    dt_css_b64 = b64encode(dt_css.encode("utf-8")).decode("ascii")

    init_notebook_mode = read_package_file("html/init_notebook_offline.html")
    init_notebook_mode = replace_value(
        init_notebook_mode,
        "_itables_underscore_version",
        _ITABLES_UNDERSCORE_VERSION,
        expected_count=3,
    )
    init_notebook_mode = replace_value(
        init_notebook_mode, "itables-version-ready", _ITABLES_READY_EVENT
    )
    init_notebook_mode = replace_value(init_notebook_mode, "dt_src_b64", dt_src_b64)
    init_notebook_mode = replace_value(init_notebook_mode, "dt_css_b64", dt_css_b64)

    return (
        init_notebook_mode
        + f"""
<div style="vertical-align:middle; text-align:left">
<noscript>
{get_animated_logo(opt.display_logo_when_loading)}
This is the <code>init_notebook_mode</code> cell from ITables v{itables_version}<br>
(you should not see this message - is your notebook <it>trusted</it>?)
</noscript>
</div>
"""
    )


def _table_header(
    df: DataFrameOrSeries,
    df_module_name: DataFrameModuleName,
    show_index: bool,
    footer: Union[bool, str],
    column_filters: Literal["header", "footer", False],
    escape_html: bool,
    show_dtypes: bool,
):
    """This function returns the HTML table header. Rows are not included."""
    # Generate table head using pandas.to_html(), see issue 63
    pattern = re.compile(r".*<thead>(.*)</thead>", flags=re.MULTILINE | re.DOTALL)
    if df_module_name in ["pandas", "numpy"]:
        html_header = df.head(0).to_html(escape=escape_html)
    else:
        # Polars or Narwhalified DataFrame
        columns = [escape_html_chars(col) if escape_html else col for col in df.columns]
        formatted_columns = "".join(f"<th>{col}</th>" for col in columns)
        html_header = f'<table class="dataframe">\n<thead>\n<tr style="text-align: right;">\n<th></th>\n{formatted_columns}\n</tr>\n</thead>\n  <tbody>\n  </tbody>\n</table>'

    match = pattern.match(html_header)
    del html_header
    assert match is not None
    thead = match.groups()[0]
    # Don't remove the index header for empty dfs
    if not show_index and len(df.columns):
        thead = thead.replace("<th></th>", "", 1)

    # NB: The dtype row is not compatible with the footer option
    # which requires a flat header
    if show_dtypes and (footer is False):

        def format_dtype(dtype):
            if hasattr(dtype, "_string_repr"):
                return dtype._string_repr()

            # Use dtype.name for cleaner representation (e.g., "string" instead of "<StringDtype(...)>")
            if hasattr(dtype, "name"):
                dtype_str = dtype.name
            else:
                dtype_str = str(dtype)

            if dtype_str.startswith("int"):
                return "i" + dtype_str[3:]
            elif dtype_str.startswith("uint"):
                return "u" + dtype_str[4:]
            elif dtype_str.startswith("float"):
                return "f" + dtype_str[5:]
            else:
                return dtype_str

        if show_index:
            pd = sys.modules["pandas"]

            if isinstance(df.index, pd.MultiIndex):
                all_dtypes = list(df.index.dtypes) + list(df.dtypes)
            else:
                all_dtypes = [df.index.dtype] + list(df.dtypes)
        else:
            all_dtypes = df.dtypes

        column_count = _column_count_in_header(thead)
        all_dtypes = [""] * (column_count - len(all_dtypes)) + list(all_dtypes)

        formatted_dtypes = "".join(
            f"<th><small class='itables-dtype'>{escape_html_chars(format_dtype(dt)) if escape_html else dt}</small></th>"
            for dt in all_dtypes
        )
        thead = thead + f"<tr>{formatted_dtypes}</tr>"

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


def replace_value(
    template: str, pattern: str, value: str, expected_count: int = 1
) -> str:
    """Set the given pattern to the desired value in the template,
    after making sure that the pattern is found exactly once."""
    count = template.count(pattern)
    if count != expected_count:
        raise ValueError(
            f"{pattern=} was found {count} times in template, expected {expected_count}."
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
    fallback_html = _simple_html_table_from_dt_args(dt_args)
    return html_table_from_template(
        table_id=table_id,
        dt_url=dt_url,
        connected=connected,
        display_logo_when_loading=display_logo_when_loading,
        kwargs=dt_args,
        fallback_html=fallback_html,
    )


_STATIC_PREVIEW_HELP_URL = (
    "https://mwouts.github.io/itables/fallbacks/static_preview.html"
)
_STATIC_PREVIEW_MESSAGE = (
    f"<sup><a href={_STATIC_PREVIEW_HELP_URL} "
    f'title="ITables v{itables_version} static preview">ⓘ</a></sup>'
)


def _could_not_load_message(*, connected: bool) -> str:
    """Markdown explanation shown by show() when it can't attempt to
    display HTML/JavaScript at all - cf. #575."""
    source = "the internet" if connected else "the `init_notebook_mode` cell"
    help_link = f"[help]({_STATIC_PREVIEW_HELP_URL})"
    return (
        f"Could not load ITables v{itables_version} from {source}, "
        f"defaulting to a static preview (need {help_link}?)"
    )


# The exact 'render' function that get_itable_arguments() generates for float
# columns formatted in Python, cf. get_float_columns_to_be_formatted_in_python()
_FLOAT_SORT_PAIR_RENDER = (
    "function (data, type, row, meta) "
    "{ return type === 'sort' || type === 'type' ? data[1] : data[0]; }"
)
# The 'render' function generated for categorical columns sorted by rank,
# cf. get_categorical_columns_to_be_represented_through_their_rank(): the
# categories are embedded in the function body as a JSON array
_CATEGORY_RENDER_RE = re.compile(r"var categories = (.*); return type")
_NON_FINITE_FLOAT_SENTINELS = {
    "___NaN___": "NaN",
    "___Infinity___": "Infinity",
    "___-Infinity___": "-Infinity",
}
_THEAD_RE = re.compile(r"<thead>(.*?)</thead>", re.DOTALL)
_TR_RE = re.compile(r"<tr[^>]*>(.*?)</tr>", re.DOTALL)
_TH_RE = re.compile(r"<th[^>]*>(.*?)</th>", re.DOTALL)
_TAG_RE = re.compile(r"<[^>]+>")
_TABLE_OPEN_RE = re.compile(r"<table\b[^>]*>")
_CELL_OPEN_RE = re.compile(r"<(th|td)\b([^>]*)>")
_STYLE_ATTR_RE = re.compile(r'\sstyle="([^"]*)"')
# Light cell delimiters as inline styles rather than a <style> tag,
# which may not survive a sanitizer.
_TABLE_STYLE = "border-collapse:collapse"
_CELL_STYLE = "border:1px solid #ddd;padding:8px"


def _markdown_escape_cell(value: str) -> str:
    """Escape a cell value so that it can't break out of a Markdown table row"""
    return value.replace("|", "\\|").replace("\n", " ")


def _markdown_table(headers: Sequence[str], rows: Sequence[Sequence[str]]) -> str:
    """Format a column-aligned GitHub-Flavored-Markdown table"""
    header_cells = [_markdown_escape_cell(h) for h in headers] or [""]
    row_cells = [[_markdown_escape_cell(cell) for cell in row] for row in rows]

    widths = [len(cell) for cell in header_cells]
    for row in row_cells:
        for i, cell in enumerate(row):
            if i < len(widths):
                widths[i] = max(widths[i], len(cell))

    def format_row(cells: Sequence[str]) -> str:
        cells = cells or [""] * len(widths)
        return (
            "| "
            + " | ".join(cell.ljust(width) for cell, width in zip(cells, widths))
            + " |"
        )

    lines = [
        format_row(header_cells),
        "| " + " | ".join("-" * w for w in widths) + " |",
    ]
    lines.extend(format_row(row) for row in row_cells)
    return "\n".join(lines)


def _rows_per_page(dt_args: Mapping[str, Any]) -> Optional[int]:
    """Return the number of rows to show in the Markdown fallback table,
    following the pagination options ('paging', 'pageLength', 'lengthMenu').
    Returns None if all the (downsampled) rows should be shown."""
    if dt_args.get("paging") is False:
        return None

    page_length = dt_args.get("pageLength")
    if isinstance(page_length, (int, float)) and page_length > 0:
        return int(page_length)

    min_rows = _min_rows(dt_args)
    return int(min_rows) if isinstance(min_rows, (int, float)) else 10


def _header_labels_from_table_html(table_html: str) -> "list[str]":
    """Extract the plain-text column labels from the <thead> of an
    itables-generated table_html string.

    A named index gets its own header row (name under the index column,
    blanks elsewhere), so we merge all the (non-dtype) rows column-by-
    column rather than just taking the first one. NB: for a Pandas
    MultiIndex, colspan-ed labels aren't expanded, so some may be lost.
    """
    thead_match = _THEAD_RE.search(table_html)
    if not thead_match:
        return []

    rows = [
        [_TAG_RE.sub("", cell).strip() for cell in _TH_RE.findall(row)]
        for row in _TR_RE.findall(thead_match.group(1))
        # The dtypes sub-header added by show_dtypes isn't a column label
        if "itables-dtype" not in row
    ]
    if not rows:
        return []

    width = max(len(row) for row in rows)
    if any(len(row) != width for row in rows):
        # Rows disagree on the number of cells (e.g. a Pandas MultiIndex,
        # where the outer levels use colspan): fall back to the last row,
        # which has one cell per column
        return rows[-1]

    return [next((cell for cell in column if cell), "") for column in zip(*rows)]


def _float_and_category_targets_from_column_defs(
    columnDefs: Optional[Sequence[Mapping[str, Any]]],
) -> "tuple[set[int], dict[int, list]]":
    """Recover, from the columnDefs generated by get_itable_arguments(), which
    columns are float columns encoded as [display, sort] pairs, and which
    columns are categorical columns encoded as a 1-based rank (0 = missing),
    together with their ordered list of categories."""
    float_targets: set[int] = set()
    category_targets: dict[int, list] = {}
    for col_def in columnDefs or []:
        targets = col_def.get("targets")
        target_list = cast(
            "list[int]", targets if isinstance(targets, list) else [targets]
        )
        render = str(col_def.get("render", ""))
        if render == _FLOAT_SORT_PAIR_RENDER:
            float_targets.update(target_list)
            continue
        match = _CATEGORY_RENDER_RE.search(render)
        if match:
            categories = json.loads(match.group(1))
            for target in target_list:
                category_targets[target] = categories
    return float_targets, category_targets


def _decode_cell_for_markdown(
    value: Any, *, is_float: bool, categories: Optional[list]
) -> str:
    """Turn one data_json cell (as produced by get_itable_arguments(), see
    datatables_rows()) into a plain-text value for the Markdown table."""
    if is_float:
        # [display_string, sort_value] pair, cf. _FLOAT_SORT_PAIR_RENDER above
        display_value = None if value is None else value[0]
        return "" if display_value is None else str(display_value)
    if categories is not None:
        # 1-based rank (0 = missing), cf. add_rank_to_categories
        return "" if not value else str(categories[value - 1])
    if value is None:
        return ""
    if isinstance(value, str) and value in _NON_FINITE_FLOAT_SENTINELS:
        return _NON_FINITE_FLOAT_SENTINELS[value]
    return str(value)


def _decoded_rows(dt_args: DTForITablesOptions) -> "tuple[list[list[str]], int]":
    """Decode dt_args['data_json'] into plain-text rows, truncated to the
    pagination row count. Returns (rows, hidden_row_count), where
    hidden_row_count counts every row missing from the preview compared to
    the original dataframe - both the ones downsampling already dropped
    from data_json (filtered_row_count) and the ones pagination hides on
    top of that."""
    float_targets, category_targets = _float_and_category_targets_from_column_defs(
        dt_args.get("columnDefs")
    )
    all_rows = json.loads(cast(str, dt_args.get("data_json")))
    text_rows = [
        [
            _decode_cell_for_markdown(
                cell,
                is_float=i in float_targets,
                categories=category_targets.get(i),
            )
            for i, cell in enumerate(row)
        ]
        for row in all_rows
    ]

    total_rows = len(text_rows)
    rows_to_show = _rows_per_page(dt_args)
    hidden_rows = cast(int, dt_args.get("filtered_row_count", 0))
    if rows_to_show is not None and rows_to_show < total_rows:
        text_rows = text_rows[:rows_to_show]
        hidden_rows += total_rows - rows_to_show

    return text_rows, hidden_rows


def _fallback_notes(dt_args: DTForITablesOptions, hidden_rows: int) -> "list[str]":
    """Return the small, human-readable notes (rows/columns missing from
    the preview, out of the original dataframe) that go along with a
    static fallback table."""
    hidden_columns = cast(int, dt_args.get("filtered_column_count", 0))
    downsampled = bool(
        cast(int, dt_args.get("filtered_row_count", 0)) or hidden_columns
    )
    notes = []
    if not downsampled and dt_args.get("downsampling_warning"):
        # show_df_type=True stashes the dataframe type description in
        # downsampling_warning even when nothing was actually downsampled
        # (cf. get_itable_arguments()) - show it here, since it's then just
        # that description, not the (now redundant) downsampling message.
        # It must be checked independently of hidden_rows/hidden_columns
        # below, since those may be nonzero from pagination alone.
        notes.append(cast(str, dt_args.get("downsampling_warning")))
    row_note = (
        f"{hidden_rows:,d} more row{'s' if hidden_rows > 1 else ''}"
        if hidden_rows > 0
        else ""
    )
    col_note = (
        f"{hidden_columns:,d} more column{'s' if hidden_columns > 1 else ''}"
        if hidden_columns > 0
        else ""
    )
    if row_note and col_note:
        notes.append(f"{row_note} and {col_note} not shown")
    elif row_note or col_note:
        notes.append(f"{row_note or col_note} not shown")
    return notes


def to_markdown_table(
    df: DataFrameOrSeries,
    caption: Optional[str] = None,
    **kwargs: Unpack[ITableOptions],
) -> str:
    """
    Return a simple, static Markdown table for the given dataframe. This is
    what show() prints when it can't display an interactive table at all
    (cf. #575). Only the first rows are included, following the pagination
    options ('pageLength', 'lengthMenu' or 'paging') - 10 rows by default.
    """
    # get_itable_arguments() expects a resolved table_id, cf. to_html_datatable()
    kwargs["table_id"] = check_table_id(kwargs.pop("table_id", None), kwargs, df=df)
    dt_args = get_itable_arguments(df, **kwargs)
    return _markdown_table_from_dt_args(dt_args, caption)


def _markdown_table_from_dt_args(
    dt_args: DTForITablesOptions, caption: Optional[str]
) -> str:
    """Build the Markdown table (see to_markdown_table()) from the output of
    get_itable_arguments(). Just the table: show() prepends its own "could
    not load" explanation when actually falling back to it."""
    lines = []
    if caption:
        lines.append(f"**{caption}**")
        lines.append("")

    if "data_json" not in dt_args:
        # df is None, or this is a Pandas Styler object (or use_to_html=True
        # in general), rendered with df.to_html() directly: there is no
        # downsampled, DataTables-ready data to build a Markdown preview from
        lines.append("*(no static preview available for this table)*")
        return "\n".join(lines)

    headers = _header_labels_from_table_html(cast(str, dt_args.get("table_html")))
    text_rows, hidden_rows = _decoded_rows(dt_args)
    lines.append(_markdown_table(headers, text_rows))

    notes = _fallback_notes(dt_args, hidden_rows)
    if notes:
        lines.append("")
        lines.append(f"*({'; '.join(notes)})*")

    return "\n".join(lines)


def _add_cell_borders(html: str) -> str:
    """Add a light inline border/padding style to every <th>/<td> cell in
    html (merging into any style attribute already there, e.g. a Pandas
    Styler's own cell formatting, rather than adding a second, conflicting
    style attribute)."""

    def add_style(m: "re.Match[str]") -> str:
        tag, attrs = m.group(1), m.group(2)
        style_match = _STYLE_ATTR_RE.search(attrs)
        if style_match:
            attrs = _STYLE_ATTR_RE.sub(
                f' style="{_CELL_STYLE};{style_match.group(1)}"', attrs, count=1
            )
            return f"<{tag}{attrs}>"
        return f'<{tag} style="{_CELL_STYLE}"{attrs}>'

    return _CELL_OPEN_RE.sub(add_style, html)


def _table_caption(caption: Optional[str]) -> str:
    """Wrap the original table caption (if any) in a <caption> tag, part of
    the <table> so it stays aligned the same way as the table itself,
    regardless of whatever CSS the surrounding page applies to it."""
    return f"<caption>{caption}</caption>" if caption else ""


def _caption_side(dt_args: DTForITablesOptions) -> str:
    """The 'caption-side' from the DataTable style (bottom by default), which
    tells us where to place the caption row in the static preview - matching
    where the interactive table shows its caption."""
    for part in cast(str, dt_args.get("style") or "").split(";"):
        prop, _, value = part.partition(":")
        if prop.strip() == "caption-side" and value.strip():
            return value.strip()
    return "bottom"


_CAPTION_RE = re.compile(r"<caption[^>]*>(.*?)</caption>", re.DOTALL)


def _caption_as_row(
    table_html: str, col_count: int, side: str, notes: "list[str]"
) -> str:
    """Turn the <caption> element and the downsampling/hidden-row notes (if
    any), into one spanning, borderless table row. We can't keep a real
    <caption>: GitHub's notebook-output sanitizer strips <caption> tags, and
    the leftover text is then foster-parented out of the table by the HTML
    parser, landing *above* it - so with the default caption-side:bottom the
    caption would end up on the wrong side. A <tr>/<td> row instead survives
    sanitization and stays where we put it: a <tfoot> row for
    caption-side:bottom, or a leading <thead> row for caption-side:top. This
    also rescues a caption set on a Pandas Styler via set_caption().

    The notes, if any, always come in parentheses, on their own line below
    the caption (or alone, if there is no caption)."""
    m = _CAPTION_RE.search(table_html)
    caption = m.group(1).strip() if m else None
    if m:
        table_html = table_html[: m.start()] + table_html[m.end() :]
    note = f"({'; '.join(notes)})" if notes else None
    content = "<br>".join(part for part in (caption, note) if part)
    if not content:
        return table_html
    row = (
        f'<tr><td colspan="{col_count}" '
        f'style="border:none;padding:8px;text-align:center">{content}</td></tr>'
    )
    if side == "top":
        if "<thead>" in table_html:
            return table_html.replace("<thead>", f"<thead>{row}", 1)
        return _TABLE_OPEN_RE.sub(
            lambda mm: mm.group(0) + f"<thead>{row}</thead>", table_html, count=1
        )
    # bottom (the default): a <tfoot> row, before any pre-existing one (e.g.
    # a column_filters="footer" row)
    if "<tfoot>" in table_html:
        return table_html.replace("<tfoot>", f"<tfoot>{row}", 1)
    return table_html.replace("</table>", f"<tfoot>{row}</tfoot></table>", 1)


_FIRST_TH_RE = re.compile(r"<th\b([^>]*)>(.*?)</th>", re.DOTALL)


def _add_static_preview_marker(html: str) -> str:
    """Add the static-preview marker - a small, linked 'ⓘ' with a title
    tooltip - to the first header cell, rather than a sentence of
    always-visible text in the table's footer: now that it's just that one
    symbol, it reads more naturally right where a reader's eye starts - ahead
    of that cell's own text, so it's the first thing read."""

    def add_marker(m: "re.Match[str]") -> str:
        attrs, content = m.group(1), m.group(2)
        return f"<th{attrs}>{_STATIC_PREVIEW_MESSAGE}{content}</th>"

    return _FIRST_TH_RE.sub(add_marker, html, count=1)


def _simple_html_table_from_dt_args(dt_args: DTForITablesOptions) -> str:
    """Build a plain HTML <table> (no DataTables, no JavaScript) that is
    shown by default, ahead of the interactive table - see
    to_html_datatable() and #575. This reuses table_html's <thead> as-is,
    unlike to_markdown_table(). The original caption (if any) and the
    downsampling/hidden-row notes (if any) share one spanning <tfoot>/<thead>
    row (see _caption_as_row); the static-preview marker goes in the first
    header cell. The table gets light cell delimiters via inline styles (not
    a <style> tag, which may not survive a sanitizer), so it's readable even
    with no surrounding stylesheet."""
    caption_html = _table_caption(cast(Optional[str], dt_args.get("caption")))

    if "data_json" not in dt_args:
        # df is None, or this is a Pandas Styler object (or use_to_html=True
        # in general): there is no downsampled JSON data to build a table
        # from, but table_html - when there's a df - already holds the
        # full rendered table (unstyled, for a Styler), so reuse it as-is
        # rather than showing nothing.
        table_html = dt_args.get("table_html")
        if not table_html:
            return ""
        table_html = _TABLE_OPEN_RE.sub(
            lambda m: m.group(0) + caption_html, cast(str, table_html), count=1
        )
        table_html = table_html.replace("<table", f'<table style="{_TABLE_STYLE}"', 1)
        table_html = _add_cell_borders(table_html)
        table_html = _add_static_preview_marker(table_html)
        col_count = (
            len(_header_labels_from_table_html(cast(str, dt_args.get("table_html"))))
            or 1
        )
        return _caption_as_row(table_html, col_count, _caption_side(dt_args), [])

    thead_match = _THEAD_RE.search(cast(str, dt_args.get("table_html")))
    if thead_match:
        # _table_header() can leave a blank line where an empty index
        # <th></th> was removed (show_index=False): harmless in the
        # interactive table, since DataTables re-renders the header, but
        # visible as stray whitespace in our raw-HTML fallback.
        thead_content = "\n".join(
            line for line in thead_match.group(1).splitlines() if line.strip()
        )
        thead = f"<thead>{thead_content}</thead>"
    else:
        thead = ""

    text_rows, hidden_rows = _decoded_rows(dt_args)
    body_rows = "\n".join(
        "<tr>" + "".join(f"<td>{cell}</td>" for cell in row) + "</tr>"
        for row in text_rows
    )

    table_html = (
        f'<table style="{_TABLE_STYLE}">{caption_html}{thead}<tbody>\n{body_rows}'
        "\n</tbody></table>"
    )
    table_html = _add_cell_borders(table_html)
    table_html = _add_static_preview_marker(table_html)
    col_count = (
        len(_header_labels_from_table_html(cast(str, dt_args.get("table_html")))) or 1
    )
    notes = _fallback_notes(dt_args, hidden_rows)
    return _caption_as_row(table_html, col_count, _caption_side(dt_args), notes)


def to_html_static_preview(
    df: DataFrameOrSeries,
    caption: Optional[str] = None,
    **kwargs: Unpack[ITableOptions],
) -> str:
    """
    Return the static HTML preview table for the given dataframe - the same
    plain <table> that to_html_datatable() shows by default, ahead of the
    interactive table (cf. #575). Only the first rows are included, following the pagination
    options ('pageLength', 'lengthMenu' or 'paging') - 10 rows by default.
    """
    kwargs["table_id"] = check_table_id(kwargs.pop("table_id", None), kwargs, df=df)
    dt_args = get_itable_arguments(df, caption, **kwargs)
    return _simple_html_table_from_dt_args(dt_args)


def _evaluate_show_index(df, showIndex) -> bool:
    """
    We don't want to show trivial indices (RangeIndex with no name) on Pandas DataFrames.
    """
    if df is None:
        return False
    df_module_name, df_type_name = get_dataframe_module_and_type_name(df)
    if df_module_name != "pandas":
        return False
    if showIndex != "auto":
        return showIndex
    if df_type_name == "Styler":
        return _evaluate_show_index(
            df.data,  # pyright: ignore[reportAttributeAccessIssue]
            showIndex,
        )
    if df.index.name is not None:
        return True

    import pandas as pd

    return not isinstance(df.index, pd.RangeIndex)


def _evaluate_show_dtypes(
    df_module_name: DataFrameModuleName,
    show_dtypes: Union[bool, Literal["auto"]],
) -> bool:
    """
    Determine whether to show dtypes in the table header.
    """
    if show_dtypes != "auto":
        return show_dtypes
    if df_module_name == "polars":
        import polars as pl

        return pl.Config.state()["POLARS_FMT_TABLE_HIDE_COLUMN_DATA_TYPES"] is None
    return False


def _remove_columns_with_render_in_columndefs(
    column_set: set[int],
    n_columns: int,
    columnDefs: Sequence[Mapping[str, Any]],
) -> None:
    """Remove from column_set (in-place) any column indices covered by a render function in columnDefs."""

    def remove_if_present(target: int) -> None:
        if target < 0:
            target = n_columns + target
        column_set.discard(target)

    for col_def in columnDefs:
        if "render" not in col_def or "targets" not in col_def:
            continue
        targets = col_def["targets"]
        if targets == "_all":
            column_set.clear()
            return
        if isinstance(targets, int):
            remove_if_present(targets)
            continue
        assert isinstance(targets, list), targets
        for target in targets:
            remove_if_present(target)


def get_float_columns_to_be_formatted_in_python(
    df_module_name: DataFrameModuleName,
    df: DataFrameOrSeries,
    format_floats_in_python: Union[bool, Literal["auto"]],
    columnDefs: Optional[Sequence[Mapping[str, Any]]],
) -> set[int]:
    """
    Return the set of column indices that should have their float values formatted in Python
    """
    if format_floats_in_python is False:
        return set()

    if df_module_name in ["pandas", "numpy"]:
        float_columns_to_be_formatted_in_python = {
            i for i, dtype in enumerate(df.dtypes) if dtype.kind == "f"
        }
    elif df_module_name == "polars":
        float_columns_to_be_formatted_in_python = {
            i for i, col in enumerate(df.columns) if df[col].dtype.is_float()
        }
    else:
        import narwhals as nw

        nw_df = nw.from_native(df, eager_only=True, allow_series=True)

        float_columns_to_be_formatted_in_python = {
            i for i, col in enumerate(nw_df.columns) if nw_df[col].dtype.is_float()
        }

    if columnDefs is None or format_floats_in_python is True:
        return float_columns_to_be_formatted_in_python

    # format_floats_in_python="auto":
    # remove columns that have a render function defined
    _remove_columns_with_render_in_columndefs(
        float_columns_to_be_formatted_in_python, len(df.columns), columnDefs
    )
    return float_columns_to_be_formatted_in_python


def get_categorical_columns_to_be_represented_through_their_rank(
    df_module_name: DataFrameModuleName,
    df: DataFrameOrSeries,
    add_rank_to_categories: Union[bool, Literal["auto"]],
    columnDefs: Optional[Sequence[Mapping[str, Any]]],
) -> "dict[int, list]":
    """
    Return a dict mapping column indices to their ordered categories list,
    for categorical columns where the rank should be used for sorting.
    """
    if add_rank_to_categories is False:
        return {}

    if df_module_name == "numpy":
        return {}
    elif df_module_name == "pandas":
        pd = sys.modules["pandas"]

        categorical_columns = {
            i: x.cat.categories.tolist()
            for i, (_, x) in enumerate(df.items())
            if isinstance(x.dtype, pd.CategoricalDtype)
        }
    elif df_module_name == "polars":
        pl = sys.modules["polars"]

        categorical_columns = {
            i: df[col].cat.get_categories().to_list()
            for i, col in enumerate(df.columns)
            if df[col].dtype in (pl.Categorical, pl.Enum)
        }
    else:
        nw = sys.modules["narwhals"]

        nw_df = nw.from_native(df, eager_only=True, allow_series=True)

        categorical_columns = {
            i: nw_df[col].cat.get_categories().to_list()
            for i, col in enumerate(nw_df.columns)
            if isinstance(nw_df[col].dtype, (nw.Categorical, nw.Enum))
        }

    if columnDefs is None or add_rank_to_categories is True:
        return categorical_columns

    # add_rank_to_categories="auto": remove columns that have a render function defined
    keys = set(categorical_columns.keys())
    _remove_columns_with_render_in_columndefs(keys, len(df.columns), columnDefs)
    return {k: v for k, v in categorical_columns.items() if k in keys}


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
    df_type_description = get_dataframe_type_description(df)
    df_module_name, df_type_name = get_dataframe_module_and_type_name(df)
    if df_module_name == "narwhals":
        import narwhals as nw

        native_namespace = nw.get_native_namespace(df).__name__
        # Pandas indexes are very specific so we go back to the native dataframe
        if native_namespace == "pandas":
            df = df.to_native()
            df_module_name, df_type_name = get_dataframe_module_and_type_name(df)

    if df_module_name == "pandas" and df_type_name == "Styler":
        use_to_html = kwargs.pop("use_to_html", True)
        if not use_to_html:
            raise ValueError("We have to use df.to_html() for Pandas Styler objects")
    else:
        use_to_html = kwargs.pop("use_to_html", False)

    set_default_options(kwargs, use_to_html=use_to_html, app_mode=app_mode)

    showIndex = kwargs.pop("showIndex")

    if df_module_name == "numpy":
        import pandas as pd

        df = pd.DataFrame(df)  # type: ignore

    if df_type_name == "Series":
        df = df.to_frame()

    showIndex = _evaluate_show_index(df, showIndex)
    show_dtypes = _evaluate_show_dtypes(
        df_module_name, kwargs.pop("show_dtypes", "auto")
    )
    show_df_type = kwargs.pop("show_df_type", False)

    maxBytes = kwargs.pop("maxBytes", 0)
    maxRows = kwargs.pop("maxRows", 0)

    if "maxColumns" in kwargs:
        maxColumns = kwargs.pop("maxColumns")
    elif df_module_name == "pandas":
        import pandas as pd

        maxColumns = pd.get_option("display.max_columns") or 0
    elif df_module_name == "polars":
        import polars as pl

        max_columns = cast(Union[int, None], pl.Config.state()["POLARS_FMT_MAX_COLS"])
        maxColumns = max_columns or 0
    else:
        maxColumns = 0

    if df is not None and df_module_name not in ["pandas", "polars", "numpy"]:
        try:
            import narwhals as nw
        except ImportError as e:
            raise TypeError(
                "Narwhals is required to render DataFrames other than Pandas or Polars"
            ) from e
        else:
            df = nw.from_native(df, eager_only=True, allow_series=True)

    warn_on_unexpected_types = kwargs.pop("warn_on_unexpected_types", False)
    allow_html = kwargs.pop("allow_html")

    if (
        df is not None
        and not showIndex
        and df_module_name == "pandas"
        and df_type_name != "Styler"
    ):
        import pandas as pd

        df = df.set_index(pd.RangeIndex(len(df.index)))

    table_id = kwargs.pop("table_id", None)
    footer = kwargs.pop("footer", False)
    format_floats_in_python = kwargs.pop("format_floats_in_python", "auto")
    add_rank_to_categories = kwargs.pop("add_rank_to_categories", "auto")
    warn_on_selected_rows_not_rendered = kwargs.pop(
        "warn_on_selected_rows_not_rendered", False
    )
    warn_on_polars_get_fmt_not_found = kwargs.pop(
        "warn_on_polars_get_fmt_not_found", True
    )
    css = kwargs.pop("css", "")
    dt_args = cast(DTForITablesOptions, kwargs)
    if caption is not None:
        dt_args["caption"] = caption
    del kwargs

    if df is None:
        pass
    elif not use_to_html:
        full_row_count = len(df)  # type: ignore
        full_column_count = len(df.columns)  # type: ignore
        df, downsampling_warning = downsample(
            df,
            df_module_name=df_module_name,
            max_rows=maxRows,
            max_columns=maxColumns,
            max_bytes=maxBytes,
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
            dt_args["filtered_column_count"] = full_column_count - len(df.columns)

        if dt_args.get("column_filters", False) == "footer":
            footer = True

        table_header = _table_header(
            df,
            df_module_name,
            showIndex,
            footer,
            dt_args.get("column_filters", False),
            escape_html=allow_html is not True,
            show_dtypes=show_dtypes,
        )

        # Export the table data to JSON and include this in the HTML
        if showIndex:
            df = safe_reset_index(df)

        # When the header has an extra column, we add
        # an extra empty column in the table data #141
        column_count = _column_count_in_header(table_header)
        dt_args["table_html"] = table_header
        columnDefs = dt_args.get("columnDefs") or []
        float_columns_to_be_formatted_in_python: set[int] = (
            get_float_columns_to_be_formatted_in_python(
                df_module_name, df, format_floats_in_python, columnDefs
            )
        )
        categorical_columns = (
            get_categorical_columns_to_be_represented_through_their_rank(
                df_module_name, df, add_rank_to_categories, columnDefs
            )
        )
        dt_args["data_json"] = datatables_rows(
            df,
            column_count=column_count,
            escape_html=allow_html is not True,
            float_columns_to_be_formatted_in_python=float_columns_to_be_formatted_in_python,
            categorical_columns_to_be_represented_through_their_rank=set(
                categorical_columns.keys()
            ),
            warn_on_unexpected_types=warn_on_unexpected_types,
            warn_on_polars_get_fmt_not_found=warn_on_polars_get_fmt_not_found,
        )
        col_offset = column_count - len(df.columns)
        extra_column_defs = []
        if float_columns_to_be_formatted_in_python:
            extra_column_defs.append(
                {
                    "targets": [
                        i + col_offset for i in float_columns_to_be_formatted_in_python
                    ],
                    "render": JavascriptFunction(
                        "function (data, type, row, meta) { return type === 'sort' || type === 'type' ? data[1] : data[0]; }"
                    ),
                }
            )
        for col_idx, categories in sorted(categorical_columns.items()):
            if allow_html is not True:
                categories = [escape_html_chars(cat) for cat in categories]
            extra_column_defs.append(
                {
                    "targets": col_idx + col_offset,
                    "render": JavascriptFunction(
                        f"""function (data, type, row, meta) {{ var categories = {json.dumps(categories)}; return type === 'sort' ? data : (data === 0 ? null : categories[data - 1]); }}"""
                    ),
                }
            )
        if extra_column_defs:
            dt_args["columnDefs"] = extra_column_defs + list(columnDefs)
    else:
        if df_module_name == "pandas" and df_type_name == "Styler":
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

    if css:
        # We embed the CSS in the table's own output (rather than relying on a
        # separate display(HTML(...)) cell) so that it is guaranteed to render
        # together with the table, see https://github.com/mwouts/itables/issues/572
        table_style = dt_args.get("table_style")
        dt_args["table_style"] = f"{css}\n{table_style}" if table_style else css

    if show_df_type:
        if "downsampling_warning" in dt_args:
            downsampling_warning = dt_args["downsampling_warning"]
            downsampling_warning = f"{df_type_description} {downsampling_warning}"
            dt_args["downsampling_warning"] = downsampling_warning
        else:
            dt_args["downsampling_warning"] = df_type_description
            dt_args["filtered_row_count"] = 0

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
        df_module_name = type(df).__module__.split(".")[0]
        df_type_name = type(df).__name__

        if df_module_name == "pandas" and df_type_name == "Styler":
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
        if option.startswith("_"):
            continue
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
    fallback_html: str = "",
) -> str:
    # Load the HTML template
    if connected:
        output = read_package_file("html/datatables_template.html")
        assert dt_url.endswith(".js")
        output = replace_value(output, UNPKG_DT_BUNDLE_URL_NO_VERSION, dt_url)
        output = replace_value(
            output,
            UNPKG_DT_BUNDLE_CSS_NO_VERSION,
            dt_url[:-3] + ".css",
        )
    else:
        output = read_package_file("html/datatables_template_offline.html")
        output = replace_value(
            output,
            "_itables_underscore_version",
            _ITABLES_UNDERSCORE_VERSION,
            expected_count=2,
        )
        output = replace_value(output, "itables-version-ready", _ITABLES_READY_EVENT)

    itables_source = (
        "the internet" if connected else "the <code>init_notebook_mode</code> cell"
    )
    table_body = f"""
  <tbody>
    <tr>
      <td style="vertical-align:middle; text-align:left">{get_animated_logo(display_logo_when_loading)}
        Loading ITables v{itables_version} from {itables_source}...
        (need <a href=https://mwouts.github.io/itables/troubleshooting.html>help</a>?)
      </td>
    </tr>
  </tbody>
"""
    check_table_id(table_id, kwargs)
    # Substitute '#table_id' now, since our own fallback content below may
    # itself contain that literal text if that's the table_id in use.
    output = replace_value(output, "#table_id", f"#{table_id}")

    # Placed right after the table (not at the end of the document) so the
    # trailing <script> tag - on which shiny.py's DT() relies - is kept.
    if fallback_html:
        # The static preview is the *default*, visible content, and the
        # interactive table starts out hidden: a <noscript> fallback would
        # not work here, since e.g. GitHub's own notebook preview page runs
        # JavaScript (it's a JS-powered page), so <noscript> content never
        # renders there even though GitHub does not execute the <script>
        # tags we emit in this HTML fragment (they're inserted into the
        # page's DOM rather than parsed as part of it, so they stay inert -
        # see #587). This inline script - which only runs where scripts we
        # emit are actually executed, e.g. a real Jupyter session - swaps
        # the two around: hide the static preview, and reveal the
        # interactive table.
        # The value is written out explicitly (hidden="hidden", not a bare
        # 'hidden') because JupyterLab's untrusted-output sanitizer
        # (sanitize-html) drops attributes with an empty value even when the
        # attribute name itself is allowlisted - a valued boolean attribute
        # is equivalent per the HTML spec, but survives that sanitizer.
        table_hidden = ' hidden="hidden"'
        fallback_id = f"{table_id}_fallback"
        swap_script = (
            f"<script>"
            f'document.getElementById("{table_id}")?.removeAttribute("hidden");'
            f'document.getElementById("{fallback_id}")?.setAttribute("hidden", "hidden");'
            f"</script>"
        )
        fallback_block = f'\n<div id="{fallback_id}">{fallback_html}</div>{swap_script}'
    else:
        table_hidden = ""
        fallback_block = ""
    output = replace_value(
        output,
        '<table id="table_id"></table>',
        f'<table id="{table_id}"{table_hidden}>{table_body}</table>{fallback_block}',
    )

    assert "classes" in kwargs
    kwargs["classes"] = get_expanded_classes(kwargs["classes"])
    assert "style" in kwargs
    kwargs["style"] = get_expanded_style(kwargs["style"])

    # Export the DT args to JSON, sort keys for reproducible output
    # Format with one line per top-level key/value for readability and version control
    json_lines = ["{"]
    items = sorted(kwargs.items())
    for i, (key, value) in enumerate(items):
        value_json = json.dumps(value, sort_keys=True)
        comma = "," if i < len(items) - 1 else ""
        json_lines.append(f'  "{key}": {value_json}{comma}')
    json_lines.append("}")
    dt_args_json = "\n".join(json_lines)

    # Indent all lines after the first to align with the JavaScript code structure
    lines = dt_args_json.split("\n")
    indented_lines = [lines[0]] + ["        " + line for line in lines[1:]]
    dt_args_formatted = "\n".join(indented_lines)

    output = replace_value(
        output, "let dt_args = {};", f"let dt_args = {dt_args_formatted};"
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


def safe_reset_index(df):
    import pandas as pd

    assert isinstance(df, pd.DataFrame)
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


def _html_display_is_supported() -> bool:
    """Return True if we're running inside a Jupyter kernel that can be
    expected to run JavaScript (as opposed to no IPython at all, a plain
    Python script, or a terminal-based IPython session)."""
    try:
        from IPython import get_ipython  # pyright: ignore[reportPrivateImportUsage]
    except ImportError:
        return False

    shell = get_ipython()
    if shell is None:
        return False

    return shell.__class__.__name__ != "TerminalInteractiveShell"


def show(
    df: DataFrameOrSeries,
    caption: Optional[str] = None,
    **kwargs: Unpack[ITableOptions],
) -> None:
    """Render the given dataframe as an interactive datatable.

    When HTML/JavaScript can't be rendered (no IPython, or no JavaScript
    support, e.g. in a terminal), a simpler Markdown table is printed
    instead - see to_markdown_table()."""
    if not _html_display_is_supported():
        connected = bool(kwargs.get("connected", _CONNECTED))
        print(_could_not_load_message(connected=connected))
        print()
        print(to_markdown_table(df, caption, **kwargs))
        return

    from IPython.display import HTML, display

    display(HTML(to_html_datatable(df, caption, **kwargs)))
