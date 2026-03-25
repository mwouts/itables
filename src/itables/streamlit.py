from typing import Optional

import streamlit.components.v2 as components
from streamlit.components.v2.bidi_component import BidiComponentResult

from .javascript import get_itables_extension_arguments
from .typing import DataFrameOrSeries, ITableOptions, Unpack
from .utils import find_package_file

_component_dir = find_package_file("itables_for_streamlit")
_js_content = (_component_dir / "index.js").read_text(encoding="utf-8")
_css_content = (_component_dir / "index.css").read_text(encoding="utf-8")

_streamlit_component_func = components.component(
    "itables.itables_for_streamlit",
    js=_js_content,
    css=_css_content,
    isolate_styles=False,
)


def interactive_table(
    df: Optional[DataFrameOrSeries],
    key: Optional[str] = None,
    caption: Optional[str] = None,
    **kwargs: Unpack[ITableOptions],
) -> BidiComponentResult:
    """Render the DataFrame as an interactive datatable in Streamlit applications"""
    dt_args, other_args = get_itables_extension_arguments(df, caption, **kwargs)
    return _streamlit_component_func(
        key=key,
        data={"dt_args": dt_args, "other_args": other_args},
        default={"selected_rows": []},
    )
