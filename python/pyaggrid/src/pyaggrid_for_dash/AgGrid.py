# AUTO GENERATED FILE - DO NOT EDIT

import typing  # noqa: F401

from dash.development.base_component import Component, _explicitize_args
from typing_extensions import Literal, NotRequired, TypedDict  # noqa: F401

try:
    from dash.types import NumberType  # noqa: F401
except ImportError:
    # Backwards compatibility for dash<=4.1.0
    if typing.TYPE_CHECKING:
        raise
    NumberType = typing.Union[  # noqa: F401
        typing.SupportsFloat, typing.SupportsInt, typing.SupportsComplex
    ]

ComponentSingleType = typing.Union[str, int, float, Component, None]
ComponentType = typing.Union[
    ComponentSingleType,
    typing.Sequence[ComponentSingleType],
]


class AgGrid(Component):
    """An AgGrid component.
    AgGrid is a dash component for AG Grid

    Keyword arguments:

    - id (string; required):
        The ID used to identify this component in Dash callbacks.

    - caption (string; optional):
        The table caption.

    - classes (string; required):
        The classes of the grid container.

    - grid_args (dict; required):
        The arguments for AG Grid: the grid options, the data, and the
        optional downsampling warning.

    - selected_rows (list; required):
        The index of the selected rows (pass rowSelection to allow
        selection)."""

    _children_props: typing.List[str] = []
    _base_nodes = ["children"]
    _namespace = "pyaggrid_for_dash"
    _type = "AgGrid"

    def __init__(
        self,
        id: typing.Optional[typing.Union[str, dict]] = None,
        caption: typing.Optional[str] = None,
        selected_rows: typing.Optional[typing.Sequence] = None,
        style: typing.Optional[typing.Any] = None,
        classes: typing.Optional[str] = None,
        grid_args: typing.Optional[dict] = None,
        **kwargs
    ):
        self._prop_names = [
            "id",
            "caption",
            "classes",
            "grid_args",
            "selected_rows",
            "style",
        ]
        self._valid_wildcard_attributes = []
        self.available_properties = [
            "id",
            "caption",
            "classes",
            "grid_args",
            "selected_rows",
            "style",
        ]
        self.available_wildcard_properties = []
        _explicit_args = kwargs.pop("_explicit_args")
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        for k in ["id", "classes", "grid_args", "selected_rows", "style"]:
            if k not in args:
                raise TypeError("Required argument `" + k + "` was not specified.")

        super(AgGrid, self).__init__(**args)


setattr(AgGrid, "__init__", _explicitize_args(AgGrid.__init__))
