# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


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
    selection).

- style (dict; required):
    The table style."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'itables_for_dash'
    _type = 'ITable'
    @_explicitize_args
    def __init__(self, id=Component.REQUIRED, data=Component.REQUIRED, columns=Component.REQUIRED, caption=Component.UNDEFINED, selected_rows=Component.REQUIRED, style=Component.REQUIRED, classes=Component.REQUIRED, dt_args=Component.REQUIRED, filtered_row_count=Component.REQUIRED, downsampling_warning=Component.REQUIRED, **kwargs):
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
