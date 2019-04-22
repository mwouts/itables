"""Global options for the Interactive Tables"""

"""Show the index? Possible values: True, False and 'auto'. In mode 'auto', the index is not shown
if it has no name and its content is range(N)"""
showIndex = 'auto'

"""Default styling options. See https://datatables.net/manual/styling/classes"""
classes = ['display']

"""Maximum bytes for displaying a table"""
maxBytes = 2 ** 20
