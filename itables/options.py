"""Global options for the Interactive Tables.

These parameters are documented at
https://mwouts.github.io/itables/advanced_parameters.html
"""
from .utils import read_package_file

"""Show the index? Possible values: True, False and 'auto'. In mode 'auto', the index is not shown
if it has no name and its content is range(N)"""
showIndex = "auto"

"""Default datatables classes. See https://datatables.net/manual/styling/classes"""
classes = "display nowrap"

"""Default table style. Use
- 'table-layout:auto' to compute the layout automatically
- 'width:auto' to fit the table width to its content
- 'margin:auto' to center the table.
Combine multiple options using ';'."""
style = "table-layout:auto;width:auto;margin:auto;caption-side:bottom"

"""Additional tags like e.g. caption"""
tags = ""

"""Maximum bytes before downsampling a table"""
maxBytes = 2**16

"""Maximum number of rows or columns before downsampling a table"""
maxRows = 0
maxColumns = 200

"""By default we don't sort the table"""
order = []

"""Pre dt code"""
pre_dt_code = ""

"""Optional table footer"""
footer = False

"""Column filters"""
column_filters = False

"""Table CSS"""
css = read_package_file("html/itables.css")

"""Should a warning appear when we have to encode an unexpected type?"""
warn_on_unexpected_types = True

"""Should a warning appear when we convert large integers to str?"""
warn_on_int_to_str_conversion = True
