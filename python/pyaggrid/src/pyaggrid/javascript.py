"""HTML/js representation of Pandas and Polars dataframes using AG Grid"""

import json
import re
import uuid
from importlib.util import find_spec
from typing import Any, Optional, cast

import pyaggrid.options as opt
from itables_core.downsample import downsample
from itables_core.formatting import datatables_rows, get_keys_to_be_evaluated
from itables_core.frames import evaluate_show_index, safe_reset_index
from itables_core.typing import (
    get_dataframe_module_and_type_name,
    get_dataframe_type_description,
)
from itables_core.utils import replace_value

from .typing import (
    DataFrameOrSeries,
    PyAgGridOptions,
    PyAgGridRendererOptions,
    Unpack,
    check_pyaggrid_arguments,
)
from .utils import read_package_file
from .version import __version__ as pyaggrid_version

_ORIGINAL_REPR_HTML = {}

# The options of 'to_html_aggrid' that are not
# passed to the AG Grid constructor
_PYAGGRID_ONLY_OPTIONS = {
    "classes",
    "style",
    "showIndex",
    "show_df_type",
    "maxBytes",
    "maxRows",
    "maxColumns",
    "table_id",
    "ag_grid_url",
    "theme",
    "warn_on_unexpected_types",
    "warn_on_polars_get_fmt_not_found",
    "warn_on_undocumented_option",
    "warn_on_unexpected_option_type",
}

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
        return "pyaggrid_" + str(uuid.uuid4()).replace("-", "_")

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


def get_pyaggrid_arguments(
    df: DataFrameOrSeries,
    caption: Optional[str] = None,
    **kwargs: Unpack[PyAgGridOptions],
) -> "dict[str, Any]":
    """
    Return the arguments to be passed to the pyaggrid HTML template:
    'table_id', 'classes', 'style', 'ag_grid_url', and the
    PyAgGridRendererOptions in 'grid_args'.
    """
    set_default_options(kwargs)

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

    table_id = check_table_id(cast(Optional[str], kwargs.pop("table_id", None)))
    classes = get_compact_classes(kwargs.pop("classes"))
    style = get_compact_style(kwargs.pop("style"))
    theme = kwargs.pop("theme")
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

    if show_index and df_module_name == "pandas":
        df = safe_reset_index(df)

    columns = [
        " / ".join(str(level) for level in col) if isinstance(col, tuple) else str(col)
        for col in df.columns
    ]

    data_json = datatables_rows(
        df,
        escape_html=False,
        warn_on_unexpected_types=warn_on_unexpected_types,
        warn_on_polars_get_fmt_not_found=warn_on_polars_get_fmt_not_found,
    )

    grid_options = cast("dict[str, Any]", kwargs)

    # Show the table on a single page when it fits
    if grid_options.get("pagination") and full_row_count <= grid_options.get(
        "paginationPageSize", 100
    ):
        grid_options["pagination"] = False

    if not grid_options.get("pagination"):
        grid_options.pop("pagination", None)
        grid_options.pop("paginationPageSize", None)
        grid_options.pop("paginationPageSizeSelector", None)

    grid_args: "dict[str, Any]" = {
        "columns": columns,
        "data_json": data_json,
        "grid_options": grid_options,
        "theme": theme,
    }

    if caption is not None:
        grid_args["caption"] = caption

    if show_df_type:
        if downsampling_warning:
            downsampling_warning = f"{df_type_description} {downsampling_warning}"
        else:
            downsampling_warning = df_type_description

    if downsampling_warning:
        grid_args["downsampling_warning"] = downsampling_warning

    keys_to_be_evaluated = get_keys_to_be_evaluated(grid_options)
    if keys_to_be_evaluated:
        grid_args["keys_to_be_evaluated"] = keys_to_be_evaluated

    return {
        "table_id": table_id,
        "classes": classes,
        "style": style,
        "ag_grid_url": ag_grid_url,
        "grid_args": grid_args,
    }


def to_html_aggrid(
    df: DataFrameOrSeries,
    caption: Optional[str] = None,
    **kwargs: Unpack[PyAgGridOptions],
) -> str:
    """
    Return the HTML representation of the given
    dataframe as an interactive AG Grid table
    """
    args = get_pyaggrid_arguments(df, caption, **kwargs)
    return html_table_from_template(**args)


def html_table_from_template(
    table_id: str,
    classes: str,
    style: str,
    ag_grid_url: str,
    grid_args: PyAgGridRendererOptions,
) -> str:
    output = read_package_file("html/aggrid_template.html")

    output = replace_value(
        output,
        "https://cdn.jsdelivr.net/npm/ag-grid-community/+esm",
        ag_grid_url,
    )

    table_div = (
        f'<div id="{table_id}" class="{classes}" style="{style}">'
        f"Loading pyaggrid v{pyaggrid_version}... "
        "(need <a href=https://mwouts.github.io/itables/troubleshooting.html>help</a>?)"
        "</div>"
    )
    output = replace_value(output, '<div id="table_id"></div>', table_div)
    output = replace_value(
        output,
        '"#table_id:not(.pyaggrid-rendered)"',
        f'"#{table_id}:not(.pyaggrid-rendered)"',
    )

    # Export the grid args to JSON, sort keys for reproducible output
    grid_args_json = json.dumps(grid_args, sort_keys=True, indent=2)
    output = replace_value(
        output, "let grid_args = {};", f"let grid_args = {grid_args_json};"
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
