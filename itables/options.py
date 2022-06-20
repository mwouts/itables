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

"""jQuery and datatables.net urls (used only when 'connected=True' in init_notebook_mode)"""
urls = dict(
    jquery="https://code.jquery.com/jquery-3.6.0.min.js",
    dt_mjs="https://cdn.datatables.net/1.12.1/js/jquery.dataTables.mjs",
    dt_css="https://cdn.datatables.net/1.12.1/css/jquery.dataTables.min.css",
)
