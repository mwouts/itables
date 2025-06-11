from typing import Optional

import streamlit.components.v1 as components
from streamlit.components.v1.custom_component import CustomComponent
from typing_extensions import Unpack

from .javascript import get_itables_extension_arguments
from .typing import DataFrameOrSeries, ITableOptions
from .utils import find_package_file

_streamlit_component_func = components.declare_component(
    "itables_for_streamlit", path=find_package_file("itables_for_streamlit")
)


def interactive_table(
    df: Optional[DataFrameOrSeries],
    key: Optional[str] = None,
    caption: Optional[str] = None,
    **kwargs: Unpack[ITableOptions],
) -> CustomComponent:
    """Render the DataFrame as an interactive datatable in Streamlit applications"""
    dt_args, other_args = get_itables_extension_arguments(df, caption, **kwargs)
    return _streamlit_component_func(key=key, dt_args=dt_args, other_args=other_args)
