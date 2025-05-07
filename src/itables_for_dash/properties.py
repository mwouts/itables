try:
    from dash import Output, no_update  # type: ignore
except ImportError as e:
    import_error = e

    def Output(*args, **kwargs):
        raise import_error

    def no_update(*args, **kwargs):
        raise import_error


from typing import Optional

from typing_extensions import Unpack

from itables.javascript import get_itables_extension_arguments
from itables.typing import DataTableOptions, ITableOptions

ITABLE_PROPERTIES = (
    "caption",
    "style",
    "classes",
    "dt_args",
    "selected_rows",
)


def get_itable_component_kwargs(
    df=None,
    *args,
    **kwargs: Unpack[ITableOptions],
):
    dt_args, other_args = get_itables_extension_arguments(df=df, *args, **kwargs)

    style = other_args.pop("style")
    style = {key: value for key, value in [x.split(":") for x in style.split(";")]}
    style["captionSide"] = style.pop("caption-side")
    style["tableLayout"] = style.pop("table-layout")

    return {
        "dt_args": dt_args,
        "style": style,
        **other_args,
    }


def ITableOutputs(id):
    return [Output(id, key) for key in ITABLE_PROPERTIES]


def updated_itable_outputs(
    df=None,
    current_dt_args: Optional[DataTableOptions] = None,
    **kwargs: Unpack[ITableOptions],
):
    updated_properties = get_itable_component_kwargs(df, **kwargs)

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

        if current_dt_args == updated_properties["dt_args"]:
            updated_properties["dt_args"] = no_update

    ordered_list_of_updated_properties = [
        updated_properties.pop(k) for k in ITABLE_PROPERTIES
    ]

    if updated_properties:
        raise ValueError(f"Unexpected properties: {updated_properties}")

    return ordered_list_of_updated_properties
