from typing import Optional

from pyaggrid import __version__
from pyaggrid.typing import DataFrameOrSeries, PyAgGridOptions, Unpack

from .AgGrid import AgGrid as AgGridComponent
from .properties import (
    AGGRID_PROPERTIES,
    PyAgGridOutputs,
    get_aggrid_component_kwargs,
    updated_aggrid_outputs,
)

_js_dist = [
    {"namespace": "pyaggrid_for_dash", "relative_package_path": name, **kwargs}
    for name, kwargs in {
        "async-AgGrid.js": {"async": True},
        "async-AgGrid.js.map": {"dynamic": True},
        "pyaggrid_for_dash.min.js": {},
        "pyaggrid_for_dash.min.js.map": {"dynamic": True},
    }.items()
]

_css_dist = []


AgGridComponent._js_dist = _js_dist  # type: ignore
AgGridComponent._css_dist = _css_dist  # type: ignore


class AgGrid(AgGridComponent):
    """An AG Grid component for Dash"""

    def __init__(
        self,
        id: str,
        df: Optional[DataFrameOrSeries] = None,
        caption: Optional[str] = None,
        **kwargs: Unpack[PyAgGridOptions],
    ):
        """
        Initialize the AgGrid component.

        Parameters
        ----------
        id : str
            The ID of the component.
        **kwargs : dict
            Additional keyword arguments for the component.
        """
        if not isinstance(id, str):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise ValueError("The id must be a string.")
        if not id:
            raise ValueError("The id cannot be an empty string.")

        return super().__init__(  # pyright: ignore[reportUnknownMemberType]
            id=id, **get_aggrid_component_kwargs(df, caption, **kwargs)
        )


__all__ = [
    "AgGrid",
    "AGGRID_PROPERTIES",
    "PyAgGridOutputs",
    "updated_aggrid_outputs",
    "get_aggrid_component_kwargs",
    "__version__",
]
