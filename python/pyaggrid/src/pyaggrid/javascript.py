"""HTML/js representation of Pandas and Polars dataframes using AG Grid"""

import json
import re
import uuid
from importlib.util import find_spec
from typing import Any, Optional, cast

import pyaggrid.options as opt
from itables_core.downsample import downsample
from itables_core.formatting import (
    datatables_rows,
    generate_encoder,
    get_keys_to_be_evaluated,
)
from itables_core.frames import evaluate_show_index, safe_reset_index
from itables_core.typing import (
    get_dataframe_module_and_type_name,
    get_dataframe_type_description,
)
from itables_core.utils import replace_value

from .typing import (
    DataFrameOrSeries,
    PyAgGridOptions,
    Unpack,
    check_pyaggrid_arguments,
)
from .utils import read_package_file
from .version import __version__ as pyaggrid_version

_ORIGINAL_REPR_HTML = {}

_CAPTION_DIV = '<div class="pyaggrid-caption" style="text-align:center">caption</div>'
_WARNING_DIV = '<div class="pyaggrid-downsampling-warning">downsampling_warning</div>'

GOOGLE_COLAB = (find_spec("google") is not None) and (
    find_spec("google.colab") is not None
)


def init_notebook_mode(
    all_interactive: bool = True,
) -> None:
    """When all_interactive=True, activate the AG Grid representation for
    all the Pandas and Polars DataFrames and Series.

    Note: unlike pydatatables, pyaggrid does not have an offline mode yet -
    the AG Grid library is loaded from the URL in 'pyaggrid.options.ag_grid_url'.
    """
    set_pyaggrid_repr_html_methods(all_interactive)


def set_pyaggrid_repr_html_methods(all_interactive: bool) -> None:
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
            pd.DataFrame._repr_html_ = _aggrid_repr_  # type: ignore
            pd.Series._repr_html_ = _aggrid_repr_  # type: ignore
        else:
            pd.DataFrame._repr_html_ = _ORIGINAL_REPR_HTML["pd.DataFrame"]  # type: ignore
            if hasattr(pd.Series, "_repr_html_"):
                del pd.Series._repr_html_  # type: ignore

    try:
        import polars as pl
    except ImportError:
        pass
    else:
        if "pl.DataFrame" not in _ORIGINAL_REPR_HTML:
            _ORIGINAL_REPR_HTML["pl.DataFrame"] = pl.DataFrame._repr_html_  # type: ignore

        if all_interactive:
            pl.DataFrame._repr_html_ = _aggrid_repr_  # type: ignore
            pl.Series._repr_html_ = _aggrid_repr_  # type: ignore
        else:
            pl.DataFrame._repr_html_ = _ORIGINAL_REPR_HTML["pl.DataFrame"]  # type: ignore
            if hasattr(pl.Series, "_repr_html_"):
                del pl.Series._repr_html_  # type: ignore


def _aggrid_repr_(df: DataFrameOrSeries) -> str:
    return to_html_aggrid(df)


def check_table_id(table_id: Optional[str]) -> str:
    """Make sure that the table_id is a valid HTML id"""
    if table_id is None:
        return "pyaggrid_" + uuid.uuid4().hex

    if not re.match(r"[A-Za-z][-A-Za-z0-9_.]*", table_id):
        raise ValueError(
            "The id name must contain at least one character, "
            f"cannot start with a number, and must not contain whitespaces ({table_id})"
        )

    return table_id


def get_compact_classes(classes) -> str:
    """Convert a list of classes to a compact string"""
    if isinstance(classes, str):
        return classes
    elif isinstance(classes, list):
        return " ".join(classes)
    else:
        raise TypeError(f"classes must be a string or a list, not {type(classes)}")


def get_compact_style(style) -> str:
    """Convert a style to a compact string"""
    if isinstance(style, str):
        return style
    elif isinstance(style, dict):
        return ";".join(f"{k}:{v}" for k, v in style.items())
    else:
        raise TypeError(f"style must be a string or a dict, not {type(style)}")


def set_default_options(kwargs: PyAgGridOptions) -> None:
    """Complement the arguments with the default values from pyaggrid.options"""
    non_options = getattr(opt, "__non_options")
    for option in set(dir(opt)).difference(non_options).difference(kwargs):
        if option.startswith("_"):
            continue
        kwargs[option] = getattr(opt, option)

    for name, value in kwargs.items():
        if value is None:
            raise ValueError(
                "Please don't pass an option with a value equal to None ('{}=None')".format(
                    name
                )
            )

    check_pyaggrid_arguments(cast("dict[str, Any]", kwargs), PyAgGridOptions)


def _header_name(col: object) -> str:
    """Flatten MultiIndex column names (grouped column headers might come later)."""
    if isinstance(col, tuple):
        parts = [str(level) for level in col if str(level) != ""]
        return " / ".join(parts)
    return str(col)


def _numeric_columns(df: DataFrameOrSeries, df_module_name) -> "set[int]":
    """Return the indices of the numeric columns"""
    if df_module_name == "pandas":
        return {i for i, dtype in enumerate(df.dtypes) if dtype.kind in "iuf"}
    if df_module_name == "polars":
        return {i for i, col in enumerate(df.columns) if df[col].dtype.is_numeric()}
    # Narwhals DataFrame
    return {i for i, col in enumerate(df.columns) if df[col].dtype.is_numeric()}


def get_column_defs(df: DataFrameOrSeries, df_module_name) -> "list[dict[str, Any]]":
    """Return the AG Grid column definitions for the given DataFrame.

    The column definitions use positional field names ``c0``, ``c1``, ... so
    that duplicated, non-string, or dotted column names cannot confuse AG Grid;
    the actual column name is in ``headerName``.
    """
    numeric_columns = _numeric_columns(df, df_module_name)
    column_defs: "list[dict[str, Any]]" = []
    for i, col in enumerate(df.columns):
        col_def: "dict[str, Any]" = {"field": f"c{i}", "headerName": _header_name(col)}
        if i in numeric_columns:
            col_def["type"] = "rightAligned"
            col_def["filter"] = "agNumberColumnFilter"
        column_defs.append(col_def)
    return column_defs


def _script_safe(json_str: str) -> str:
    """Make a JSON string safe for inclusion in a <script> block.

    A cell value containing e.g. "</script>" must not terminate the script;
    "<\\/" is an equivalent JSON escape for "</".
    """
    return json_str.replace("</", "<\\/")


def get_pyaggrid_arguments(
    df: DataFrameOrSeries,
    caption: Optional[str] = None,
    **kwargs: Unpack[PyAgGridOptions],
) -> "dict[str, Any]":
    """
    Return the arguments to be passed to the pyaggrid HTML template:
    'table_id', 'classes', 'style', 'ag_grid_url', 'caption',
    'downsampling_warning', 'data_json' and the AG Grid options
    in 'grid_options'.
    """
    set_default_options(kwargs)
    kwargs.pop("warn_on_undocumented_option", None)
    kwargs.pop("warn_on_unexpected_option_type", None)

    df_type_description = get_dataframe_type_description(df)
    df_module_name, df_type_name = get_dataframe_module_and_type_name(df)

    if df_module_name == "narwhals":
        import narwhals as nw

        native_namespace = nw.get_native_namespace(df).__name__
        # Pandas indexes are very specific so we go back to the native dataframe
        if native_namespace == "pandas":
            df = df.to_native()
            df_module_name, df_type_name = get_dataframe_module_and_type_name(df)

    if df_module_name == "numpy":
        import pandas as pd

        df = pd.DataFrame(df)
        df_module_name = "pandas"

    if df_type_name == "Series":
        df = df.to_frame()

    if df is not None and df_module_name not in ["pandas", "polars"]:
        try:
            import narwhals as nw
        except ImportError as e:
            raise TypeError(
                "Narwhals is required to render DataFrames other than Pandas or Polars"
            ) from e
        else:
            df = nw.from_native(df, eager_only=True, allow_series=True)
            df_module_name = "narwhals"

    table_id = check_table_id(cast(Optional[str], kwargs.pop("table_id", None)))
    classes = get_compact_classes(kwargs.pop("classes"))
    style = get_compact_style(kwargs.pop("style"))
    ag_grid_url = kwargs.pop("ag_grid_url")

    show_index = evaluate_show_index(df, kwargs.pop("showIndex"))
    show_df_type = kwargs.pop("show_df_type")

    maxBytes = kwargs.pop("maxBytes", 0)
    maxRows = kwargs.pop("maxRows", 0)
    maxColumns = kwargs.pop("maxColumns", 0)

    warn_on_unexpected_types = kwargs.pop("warn_on_unexpected_types", False)
    warn_on_polars_get_fmt_not_found = kwargs.pop(
        "warn_on_polars_get_fmt_not_found", True
    )

    full_row_count = len(df)
    df, downsampling_warning = downsample(
        df,
        max_rows=maxRows,
        max_columns=maxColumns,
        max_bytes=maxBytes,
    )

    if df_module_name == "pandas":
        if show_index:
            df = safe_reset_index(df)
        else:
            df = df.reset_index(drop=True)

    # No HTML escaping: AG Grid renders cell values as text, not HTML
    data_json = datatables_rows(
        df,
        escape_html=False,
        warn_on_unexpected_types=warn_on_unexpected_types,
        warn_on_polars_get_fmt_not_found=warn_on_polars_get_fmt_not_found,
    )

    grid_options = cast("dict[str, Any]", kwargs)
    if "columnDefs" not in grid_options:
        grid_options["columnDefs"] = get_column_defs(df, df_module_name)

    # Show the table on a single page when it fits
    if grid_options.get("pagination") and full_row_count <= grid_options.get(
        "paginationPageSize", 100
    ):
        grid_options.pop("pagination", None)
        grid_options.pop("paginationPageSize", None)
        grid_options.pop("paginationPageSizeSelector", None)

    keys_to_be_evaluated = get_keys_to_be_evaluated(grid_options)
    if keys_to_be_evaluated:
        grid_options["keys_to_be_evaluated"] = keys_to_be_evaluated

    if show_df_type:
        if downsampling_warning:
            downsampling_warning = f"{df_type_description} {downsampling_warning}"
        else:
            downsampling_warning = df_type_description

    return {
        "table_id": table_id,
        "classes": classes,
        "style": style,
        "ag_grid_url": ag_grid_url,
        "caption": caption,
        "downsampling_warning": downsampling_warning,
        "data_json": data_json,
        "grid_options": grid_options,
    }


def to_html_aggrid(
    df: DataFrameOrSeries,
    caption: Optional[str] = None,
    **kwargs: Unpack[PyAgGridOptions],
) -> str:
    """
    Return the HTML representation of the given
    dataframe as an interactive AG Grid table.

    The snippet loads AG Grid Community as an ES module from the URL in
    'pyaggrid.options.ag_grid_url', so an internet connection is required
    when the table is displayed.
    """
    args = get_pyaggrid_arguments(df, caption, **kwargs)
    return html_table_from_template(**args)


def html_table_from_template(
    table_id: str,
    classes: str,
    style: str,
    ag_grid_url: str,
    caption: Optional[str],
    downsampling_warning: str,
    data_json: str,
    grid_options: "dict[str, Any]",
) -> str:
    output = read_package_file("html/aggrid_template.html")

    output = replace_value(
        output,
        "https://cdn.jsdelivr.net/npm/ag-grid-community/+esm",
        ag_grid_url,
    )

    output = replace_value(
        output,
        '<div id="table_id" style="div_style">Loading pyaggrid...</div>',
        f'<div id="{table_id}" class="{classes}" style="{style}">'
        f"Loading pyaggrid v{pyaggrid_version}... "
        "(need <a href=https://mwouts.github.io/itables/troubleshooting.html>help</a>?)"
        "</div>",
    )
    output = replace_value(
        output,
        "'#table_id:not([data-pyaggrid])'",
        f"'#{table_id}:not([data-pyaggrid])'",
    )

    if caption is not None:
        output = replace_value(
            output,
            _CAPTION_DIV,
            _CAPTION_DIV.replace("caption</div>", f"{caption}</div>"),
        )
    else:
        output = replace_value(output, f"{_CAPTION_DIV}\n", "")

    if downsampling_warning:
        output = replace_value(
            output,
            _WARNING_DIV,
            _WARNING_DIV.replace("downsampling_warning", str(downsampling_warning)),
        )
    else:
        output = replace_value(output, f"{_WARNING_DIV}\n", "")

    grid_options_json = json.dumps(
        grid_options, sort_keys=True, cls=generate_encoder(False), allow_nan=False
    )
    output = replace_value(
        output,
        "let gridOptions = {};",
        f"let gridOptions = {_script_safe(grid_options_json)};",
    )
    output = replace_value(
        output, "let data = [];", f"let data = {_script_safe(data_json)};"
    )

    return output


def show(
    df: DataFrameOrSeries,
    caption: Optional[str] = None,
    **kwargs: Unpack[PyAgGridOptions],
) -> None:
    """Render the given dataframe as an interactive AG Grid table"""
    from IPython.display import HTML, display

    display(HTML(to_html_aggrid(df, caption, **kwargs)))
