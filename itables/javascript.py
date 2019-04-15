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


def table_js_script(df, html_id=None):
    """Display the javascript code that represents a table"""
    html_id = html_id or str(uuid.uuid4())

    args = {
        'data': [[v for v in df.loc[i].values] for i in df.index],
        'columns': [{'title': col} for col in df.columns]
    }

    try:
        return """$(element).html(`'<table id=\"""" + html_id + """\"/>'`);
    
    require(["datatables"], function(datatables) {
    $(document).ready(function() {        
        $('#""" + html_id + """').DataTable( """ + json.dumps(args) + """ );
    } );
})"""
    except TypeError as error:
        warnings.warn(str(error))
        return None


def init_itables():
    """Load the datatables.net Javascript library, and activate the representation
    of Pandas dataframes as interactive tables"""
    load_datatables()
    pd.DataFrame._repr_javascript_ = table_js_script
