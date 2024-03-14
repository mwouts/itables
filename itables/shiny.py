from .javascript import to_html_datatable


def DT(df, caption=None, tableId=None, **kwargs):
    """This is a version of 'to_html_datatable' that works in Shiny applications."""
    return to_html_datatable(
        df, caption=caption, tableId=tableId, connected=True, **kwargs
    )
