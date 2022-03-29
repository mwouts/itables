"""Global options for the Interactive Tables"""

"""Show the index? Possible values: True, False and 'auto'. In mode 'auto', the index is not shown
if it has no name and its content is range(N)"""
showIndex = "auto"

"""Default styling options. See https://datatables.net/manual/styling/classes"""
classes = ["display"]

"""Default table style"""
style = "max-width:100%"

"""Additional tags like e.g. caption"""
tags = ""

"""Maximum bytes for displaying a table"""
maxBytes = 2**16

"""Maximum number of rows or columns"""
# maxRows = 10000
# maxColumns = 1000

"""DataTables imports"""
requirements = [
    "https://cdn.jsdelivr.net/npm/jquery@3.5.1/dist/jquery.min.js",
    "https://cdn.datatables.net/1.11.5/js/jquery.dataTables.min.js",
]
