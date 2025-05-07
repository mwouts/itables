# AUTO GENERATED FILE - DO NOT EDIT

import typing  # noqa: F401
from typing_extensions import TypedDict, NotRequired, Literal # noqa: F401
from dash.development.base_component import Component, _explicitize_args

ComponentType = typing.Union[
    str,
    int,
    float,
    Component,
    None,
    typing.Sequence[typing.Union[str, int, float, Component, None]],
]

NumberType = typing.Union[
    typing.SupportsFloat, typing.SupportsInt, typing.SupportsComplex
]


class ITable(Component):
    """An ITable component.
ITable is a dash component for ITables

Keyword arguments:

- id (string; required):
    The ID used to identify this component in Dash callbacks.

- caption (string; optional):
    The table caption.

- classes (string; required):
    The table classes.

- dt_args (dict; required):
    The arguments for DataTable e.g. select, buttons, layout etc.

- selected_rows (list; required):
    The index of the selected rows (pass select=True to allow
    selection)."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'itables_for_dash'
    _type = 'ITable'


    def __init__(
        self,
        id: typing.Optional[typing.Union[str, dict]] = None,
        caption: typing.Optional[str] = None,
        selected_rows: typing.Optional[typing.Sequence] = None,
        style: typing.Optional[typing.Any] = None,
        classes: typing.Optional[str] = None,
        dt_args: typing.Optional[dict] = None,
        **kwargs
    ):
        self._prop_names = ['id', 'caption', 'classes', 'dt_args', 'selected_rows', 'style']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'caption', 'classes', 'dt_args', 'selected_rows', 'style']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        for k in ['id', 'classes', 'dt_args', 'selected_rows', 'style']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')

        super(ITable, self).__init__(**args)

setattr(ITable, "__init__", _explicitize_args(ITable.__init__))
