try:
    from dash import Output, no_update
except ImportError as e:
    import_error = e

    def Output(*args, **kwargs):
        raise import_error

    def no_update(*args, **kwargs):
        raise import_error


from itables.javascript import get_itables_extension_arguments

ITABLE_PROPERTIES = (
    "data",
    "columns",
    "caption",
    "selected_rows",
    "style",
    "classes",
    "dt_args",
    "filtered_row_count",
    "downsampling_warning",
)


def get_itable_component_kwargs(df=None, caption=None, selected_rows=None, **kwargs):
    dt_args, other_args = get_itables_extension_arguments(
        df=df, caption=caption, selected_rows=selected_rows, **kwargs
    )

    style = other_args.pop("style")
    style = {key: value for key, value in [x.split(":") for x in style.split(";")]}
    style["captionSide"] = style.pop("caption-side")
    style["tableLayout"] = style.pop("table-layout")

    return {
        "data": dt_args.pop("data"),
        "columns": dt_args.pop("columns"),
        "dt_args": dt_args,
        "style": style,
        **other_args,
    }


def ITableOutputs(id):
    return [Output(id, key) for key in ITABLE_PROPERTIES]


def updated_itable_outputs(
    df=None, caption=None, selected_rows=None, current_dt_args=None, **kwargs
):
    if df is not None:
        kwargs["selected_rows"] = selected_rows

    updated_properties = get_itable_component_kwargs(df, caption=caption, **kwargs)

    if df is None:
        updated_properties["data"] = no_update
        updated_properties["columns"] = no_update
        updated_properties["filtered_row_count"] = no_update
        updated_properties["downsampling_warning"] = no_update
        updated_properties["selected_rows"] = selected_rows or []

    if current_dt_args is not None:
        if current_dt_args == updated_properties["dt_args"]:
            updated_properties["dt_args"] = no_update

    ordered_list_of_updated_properties = [
        updated_properties.pop(k) for k in ITABLE_PROPERTIES
    ]

    if updated_properties:
        raise ValueError(f"Unexpected properties: {updated_properties}")

    return ordered_list_of_updated_properties
