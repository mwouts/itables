from typing import Any, Optional, cast

from dash import Output, no_update
from typing_extensions import Unpack

from itables.javascript import (
    get_expanded_style,
    get_itables_extension_arguments,
)
from itables.typing import DataFrameOrSeries, DTForITablesOptions, ITableOptions

ITABLE_PROPERTIES = (
    "caption",
    "style",
    "classes",
    "dt_args",
    "selected_rows",
)


def get_itable_component_kwargs(
    df: Optional[DataFrameOrSeries] = None,
    caption: Optional[str] = None,
    **kwargs: Unpack[ITableOptions],
) -> dict[str, Any]:
    """
    A function that prepares the arguments for our Dash component.
    """
    dt_args, other_args = get_itables_extension_arguments(df, caption, **kwargs)

    style = get_expanded_style(other_args.pop("style"))
    for key in style:
        # transform caption-side to captionSide
        words = key.split("-")
        if len(words) > 1:
            new_key = words[0] + "".join(word.capitalize() for word in words[1:])
            style[new_key] = style.pop(key)

    return {
        "dt_args": dt_args,
        "style": style,
        **other_args,
    }


def ITableOutputs(id: str) -> list[Any]:
    """
    Return the list of Output components for the ITable component
    with the given id.
    """
    return [Output(id, key) for key in ITABLE_PROPERTIES]


def updated_itable_outputs(
    df: Optional[DataFrameOrSeries] = None,
    caption: Optional[str] = None,
    current_dt_args: Optional[DTForITablesOptions] = None,
    **kwargs: Unpack[ITableOptions],
) -> list[Any]:
    """
    Return the updated properties for the ITable component, in the same
    order as ITableOutputs.
    """
    updated_properties = get_itable_component_kwargs(df, caption, **kwargs)

    if current_dt_args is not None:
        if df is None:
            for k in {
                "columns",
                "data_json",
                "filtered_row_count",
                "downsampling_warning",
            }:
                if k in current_dt_args:
                    updated_properties["dt_args"][k] = current_dt_args[k]

        if current_dt_args == cast(DTForITablesOptions, updated_properties["dt_args"]):
            updated_properties["dt_args"] = no_update

    ordered_list_of_updated_properties = [
        updated_properties.pop(k) for k in ITABLE_PROPERTIES
    ]

    if updated_properties:
        raise ValueError(f"Unexpected properties: {updated_properties}")

    return ordered_list_of_updated_properties
