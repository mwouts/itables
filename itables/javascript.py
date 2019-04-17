import uuid
import json
import pandas as pd
import warnings
from IPython.core.display import display, Javascript


def load_datatables():
    """Load the datatables.net library, and the corresponding css"""
    display(Javascript("""require.config({
    paths: {
        datatables: '//cdn.datatables.net/1.10.19/js/jquery.dataTables.min',
    }
});

$('head').append('<link rel="stylesheet" type="text/css" \
                href = "//cdn.datatables.net/1.10.19/css/jquery.dataTables.min.css" > ');
"""))


def datatables_js_script(data=None, columns=None, html_id=None, **kwargs):
    """Return the javascript code that represents a table"""
    html_id = html_id or str(uuid.uuid4())

    if data is not None:
        kwargs['data'] = data
    if columns is not None:
        kwargs['columns'] = columns

    try:
        return """$(element).html(`<table id=\"""" + html_id + """\"/>`);

        require(["datatables"], function(datatables) {
        $(document).ready(function() {        
            table = $('#""" + html_id + """').DataTable( """ + json.dumps(kwargs) + """ );
        } );
    })"""
    except TypeError as error:
        warnings.warn(str(error))
        return None


def df_to_data_columns(df):
    """Return a dict-like representation of a data frame"""
    return {
        'data': [[v for v in df.loc[i].values] for i in df.index],
        'columns': [{'title': col} for col in df.columns]
    }


def datatables_js_script_from_df(df, html_id=None):
    """Return the javascript code that represents a table"""
    return datatables_js_script(html_id=html_id, **df_to_data_columns(df))


def show(df=None, data=None, columns=None, paging=None, **kwargs):
    """Show a dataframe"""
    if df is not None:
        kwargs.update(df_to_data_columns(df))
    if data is not None:
        kwargs['data'] = data
    if columns is not None:
        kwargs['columns'] = columns
    if paging is not None:
        kwargs['paging'] = paging
    display(Javascript(datatables_js_script(**kwargs)))


def init_itables():
    """Activate the representation of Pandas dataframes as interactive tables"""
    pd.DataFrame._repr_javascript_ = datatables_js_script_from_df
