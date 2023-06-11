from .javascript import to_html_datatable


def DT(df, caption=None, tableId=None, **kwargs):
    """This is a version of 'to_html_datatable' that works in Shiny applications.

    In these applications, jquery is already loaded, so we call 'to_html_datatable'
    with an argument 'import_jquery=False'.

    Cf. https://github.com/mwouts/itables/issues/181
    and https://github.com/rstudio/py-shiny/issues/502
    """
    return to_html_datatable(
        df,
        caption=caption,
        tableId=tableId,
        connected=True,
        import_jquery=False,
        **kwargs
    )
