from typing import Any, Optional, cast

from dash import Output, no_update
from pyaggrid.javascript import (
    get_expanded_style,
    get_pyaggrid_extension_arguments,
)
from pyaggrid.typing import (
    DataFrameOrSeries,
    PyAgGridOptions,
    Unpack,
)

AGGRID_PROPERTIES = (
    "caption",
    "style",
    "classes",
    "grid_args",
    "selected_rows",
)


def get_aggrid_component_kwargs(
    df: Optional[DataFrameOrSeries] = None,
    caption: Optional[str] = None,
    **kwargs: Unpack[PyAgGridOptions],
) -> "dict[str, Any]":
    """
    A function that prepares the arguments for our Dash component.
    """
    grid_args, other_args = get_pyaggrid_extension_arguments(df, caption, **kwargs)

    style = get_expanded_style(other_args.pop("style"))
    for key in list(style):
        # transform caption-side to captionSide
        words = key.split("-")
        if len(words) > 1:
            new_key = words[0] + "".join(word.capitalize() for word in words[1:])
            style[new_key] = style.pop(key)

    return {
        "grid_args": grid_args,
        "style": style,
        **other_args,
    }


def PyAgGridOutputs(id: str) -> "list[Any]":
    """
    Return the list of Output components for the AgGrid component
    with the given id.
    """
    return [Output(id, key) for key in AGGRID_PROPERTIES]


def updated_aggrid_outputs(
    df: Optional[DataFrameOrSeries] = None,
    caption: Optional[str] = None,
    current_grid_args: Optional["dict[str, Any]"] = None,
    **kwargs: Unpack[PyAgGridOptions],
) -> "list[Any]":
    """
    Return the updated properties for the AgGrid component, in the same
    order as PyAgGridOutputs.
    """
    updated_properties = get_aggrid_component_kwargs(df, caption, **kwargs)

    if current_grid_args is not None:
        if df is None:
            for k in {
                "data_json",
                "downsampling_warning",
            }:
                if k in current_grid_args:
                    updated_properties["grid_args"][k] = current_grid_args[k]
            grid_options = cast(
                "dict[str, Any]", updated_properties["grid_args"]["grid_options"]
            )
            if not grid_options.get("columnDefs"):
                grid_options["columnDefs"] = current_grid_args.get(
                    "grid_options", {}
                ).get("columnDefs", [])

        if current_grid_args == updated_properties["grid_args"]:
            updated_properties["grid_args"] = no_update

    ordered_list_of_updated_properties = [
        updated_properties.pop(k) for k in AGGRID_PROPERTIES
    ]

    if updated_properties:
        raise ValueError(f"Unexpected properties: {updated_properties}")

    return ordered_list_of_updated_properties
