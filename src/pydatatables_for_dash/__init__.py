from typing import Optional

from pydatatables import __version__
from pydatatables.typing import DataFrameOrSeries, PyDataTablesOptions, Unpack

from .PyDataTablesRenderer import PyDataTablesRenderer as PyDataTablesRendererComponent
from .properties import (
    ITABLE_PROPERTIES,
    PyDataTablesRendererOutputs,
    get_itable_component_kwargs,
    updated_itable_outputs,
)

_js_dist = [
    {"namespace": "pydatatables_for_dash", "relative_package_path": name, **kwargs}
    for name, kwargs in {
        "async-PyDataTablesRenderer.js": {"async": True},
        "async-PyDataTablesRenderer.js.map": {"dynamic": True},
        "pydatatables_for_dash.min.js": {},
        "pydatatables_for_dash.min.js.map": {"dynamic": True},
    }.items()
]

_css_dist = []


PyDataTablesRendererComponent._js_dist = _js_dist  # type: ignore
PyDataTablesRendererComponent._css_dist = _css_dist  # type: ignore


class PyDataTablesRenderer(PyDataTablesRendererComponent):
    """An PyDataTablesRenderer component for Dash"""

    def __init__(
        self,
        id: str,
        df: Optional[DataFrameOrSeries] = None,
        caption: Optional[str] = None,
        **kwargs: Unpack[PyDataTablesOptions],
    ):
        """
        Initialize the PyDataTablesRenderer component.

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
    "PyDataTablesRenderer",
    "ITABLE_PROPERTIES",
    "PyDataTablesRendererOutputs",
    "updated_itable_outputs",
    "__version__",
]
