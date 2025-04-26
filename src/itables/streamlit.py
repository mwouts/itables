import streamlit.components.v1 as components
from typing_extensions import Unpack

from .javascript import get_itables_extension_arguments
from .typing import ITableOptions
from .utils import find_package_file

_streamlit_component_func = components.declare_component(
    "itables_for_streamlit", path=find_package_file("itables_for_streamlit")
)


def interactive_table(df, *args, **kwargs: Unpack[ITableOptions]):
    """Render the DataFrame as an interactive datatable in Streamlit applications"""
    dt_args, other_args = get_itables_extension_arguments(df, *args, **kwargs)
    return _streamlit_component_func(dt_args=dt_args, other_args=other_args)
