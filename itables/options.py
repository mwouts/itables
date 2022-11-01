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

"""Pre dt code"""
pre_dt_code = ""

"""Optional table footer"""
footer = False

"""Column filters"""
column_filters = False

"""Table CSS"""
css = """
table th {
    text-overflow: ellipsis;
    overflow: hidden;
}

table td {
    text-overflow: ellipsis;
    overflow: hidden;
}

thead input {
    width: 100%;
    padding: 3px;
    box-sizing: border-box;
}

tfoot input {
    width: 100%;
    padding: 3px;
    box-sizing: border-box;
}
"""
