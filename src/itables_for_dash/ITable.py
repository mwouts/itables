# AUTO GENERATED FILE - DO NOT EDIT

import typing  # noqa: F401
import numbers # noqa: F401
from typing_extensions import TypedDict, NotRequired, Literal # noqa: F401
from dash.development.base_component import Component, _explicitize_args
try:
    from dash.development.base_component import ComponentType # noqa: F401
except ImportError:
    ComponentType = typing.TypeVar("ComponentType", bound=Component)


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

- columns (list; required):
    The table columns - a list of dicts with a 'title' key.

- data (list; required):
    The table data - a list of lists with the same length as the
    columns.

- downsampling_warning (string; required):
    The downsampling warning message, if any.

- dt_args (dict; required):
    The arguments for DataTable e.g. select, buttons, layout etc.

- filtered_row_count (number; required):
    How many lines of the tables are not shown due to downsampling.

- selected_rows (list; required):
    The index of the selected rows (pass select=True to allow
    selection)."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'itables_for_dash'
    _type = 'ITable'

    @_explicitize_args
    def __init__(
        self,
        id: typing.Optional[typing.Union[str, dict]] = None,
        data: typing.Optional[typing.Sequence] = None,
        columns: typing.Optional[typing.Sequence] = None,
        caption: typing.Optional[str] = None,
        selected_rows: typing.Optional[typing.Sequence] = None,
        style: typing.Optional[typing.Any] = None,
        classes: typing.Optional[str] = None,
        dt_args: typing.Optional[dict] = None,
        filtered_row_count: typing.Optional[typing.Union[int, float, numbers.Number]] = None,
        downsampling_warning: typing.Optional[str] = None,
        **kwargs
    ):
        self._prop_names = ['id', 'caption', 'classes', 'columns', 'data', 'downsampling_warning', 'dt_args', 'filtered_row_count', 'selected_rows', 'style']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'caption', 'classes', 'columns', 'data', 'downsampling_warning', 'dt_args', 'filtered_row_count', 'selected_rows', 'style']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        for k in ['id', 'classes', 'columns', 'data', 'downsampling_warning', 'dt_args', 'filtered_row_count', 'selected_rows', 'style']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')

        super(ITable, self).__init__(**args)
