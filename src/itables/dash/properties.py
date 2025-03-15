from dash import no_update

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


def get_itable_properties(df=None, caption=None, selected_rows=None, **kwargs):
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


def get_itable_properties_as_list(
    df=None, caption=None, selected_rows=None, current_dt_args=None, **kwargs
):
    if df is not None:
        kwargs["selected_rows"] = selected_rows
    as_dict = get_itable_properties(df, caption=caption, **kwargs)
    if df is None:
        as_dict["data"] = no_update
        as_dict["columns"] = no_update
        as_dict["filtered_row_count"] = no_update
        as_dict["downsampling_warning"] = no_update
        as_dict["selected_rows"] = selected_rows or []
    if current_dt_args is not None:
        if current_dt_args == as_dict["dt_args"]:
            as_dict["dt_args"] = no_update
    as_list = [as_dict.pop(k) for k in ITABLE_PROPERTIES]
    assert not as_dict
    return as_list
