import re
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

$('head').append('<style> table td { text-overflow: ellipsis; overflow: hidden; } </style>');
"""))


def datatables(df=None,
               classes=['display', 'nowrap'],
               html_id=None,
               **kwargs):
    """Return the javascript code that represents a table
    :param df: a Pandas data frame
    :param classes: classes for the html table, see https://datatables.net/manual/styling/classes
    :param html_id: a unique identifier for the table
    """

    html_id = html_id or str(uuid.uuid4())
    if isinstance(classes, list):
        classes = ' '.join(classes)

    # Generate table head using pandas.to_html()
    pattern = re.compile(r'.*<thead>(.*)</thead>', flags=re.MULTILINE | re.DOTALL)
    match = pattern.match(df.head(0).to_html())
    html_table = '<table id="' + html_id + '" class="' + classes + '"><thead>' + match.groups()[0] + '</thead></table>'

    # Table content as 'data' for DataTable
    rounded_df = df.reset_index()
    for col in rounded_df:
        if rounded_df[col].dtype.kind == 'f':
            rounded_df[col] = rounded_df[col].apply(lambda x: float(format(x, '.15g')))

    kwargs['data'] = rounded_df.values.tolist()
    try:
        dt_args = json.dumps(kwargs)
        return """$(element).html(`""" + html_table + """`);
       
               require(["datatables"], function(datatables) {
               $(document).ready(function() {        
                   table = $('#""" + html_id + """').DataTable(""" + dt_args + """ );
        } );
    })"""
    except TypeError as error:
        warnings.warn(str(error))
        return ''


def show(df=None, **kwargs):
    """Show a dataframe"""
    script = datatables(df, **kwargs)
    display(Javascript(script))


def init_itables():
    """Activate the representation of Pandas dataframes as interactive tables"""
    pd.DataFrame._repr_javascript_ = datatables
