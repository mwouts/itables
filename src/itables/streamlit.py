import streamlit.components.v1 as components

from .javascript import get_itables_extension_arguments
from .utils import find_package_file

_streamlit_component_func = components.declare_component(
    "itables_for_streamlit", path=find_package_file("itables_for_streamlit")
)


def _style_as_dict(style: str):
    """The style property in React is a mapping key->value"""
    style_dict = {}
    for key_value in style.split(";"):
        key, value = key_value.split(":")
        style_dict[key] = value
    return style_dict


def interactive_table(df, caption=None, **kwargs):
    dt_args, other_args = get_itables_extension_arguments(df, caption, **kwargs)
    other_args["style"] = _style_as_dict(other_args["style"])
    return _streamlit_component_func(dt_args=dt_args, other_args=other_args)
