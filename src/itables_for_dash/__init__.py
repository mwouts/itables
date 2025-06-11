from typing_extensions import Optional, Unpack

from itables import __version__
from itables.typing import DataFrameOrSeries, ITableOptions

from .ITable import ITable as ITableComponent
from .properties import (
    ITABLE_PROPERTIES,
    ITableOutputs,
    get_itable_component_kwargs,
    updated_itable_outputs,
)

_js_dist = [
    {"namespace": "itables_for_dash", "relative_package_path": name, **kwargs}
    for name, kwargs in {
        "async-ITable.js": {"async": True},
        "async-ITable.js.map": {"dynamic": True},
        "itables_for_dash.min.js": {},
        "itables_for_dash.min.js.map": {"dynamic": True},
    }.items()
]

_css_dist = []


ITableComponent._js_dist = _js_dist  # type: ignore
ITableComponent._css_dist = _css_dist  # type: ignore


class ITable(ITableComponent):
    """An ITable component for Dash"""

    def __init__(
        self,
        id: str,
        df: Optional[DataFrameOrSeries] = None,
        caption: Optional[str] = None,
        **kwargs: Unpack[ITableOptions],
    ):
        """
        Initialize the ITable component.

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
            id=id, **get_itable_component_kwargs(df, caption, **kwargs)
        )


__all__ = [
    "ITable",
    "ITABLE_PROPERTIES",
    "ITableOutputs",
    "updated_itable_outputs",
    "__version__",
]
