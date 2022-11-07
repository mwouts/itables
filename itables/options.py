"""Global options for the Interactive Tables"""
from .utils import read_package_file

"""Show the index? Possible values: True, False and 'auto'. In mode 'auto', the index is not shown
if it has no name and its content is range(N)"""
showIndex = "auto"

"""Default styling options. See https://datatables.net/manual/styling/classes"""
classes = ["display"]

"""Default table style"""
style = "width:auto;"

"""Additional tags like e.g. caption"""
tags = ""

"""Maximum bytes for displaying a table"""
maxBytes = 2**16

"""Maximum number of rows or columns"""
# maxRows = 10000
# maxColumns = 1000

"""Pre dt code"""
pre_dt_code = ""

"""Optional table footer"""
footer = False

"""Column filters"""
column_filters = False

"""Table CSS"""
css = read_package_file("html/itables.css")
