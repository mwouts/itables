import re
import uuid
import json
import pandas as pd
import numpy as np
import pandas.io.formats.format as fmt
import warnings
from IPython.core.display import display, Javascript

try:
    unicode  # Python 2
except NameError:
    unicode = str  # Python 3


def load_datatables():
    """Load the datatables.net library, and the corresponding css"""
    display(Javascript("""require.config({
    paths: {
        datatables: 'https://cdn.datatables.net/1.10.19/js/jquery.dataTables.min',
    }
});

$('head').append('<link rel="stylesheet" type="text/css" \
                href = "https://cdn.datatables.net/1.10.19/css/jquery.dataTables.min.css" > ');

$('head').append('<style> table td { text-overflow: ellipsis; overflow: hidden; } </style>');
"""))


def datatables(df=None,
               classes=['display'],
               html_id=None,
               show_index='auto',
               max_bytes=2 ** 20,
               **kwargs):
    """Return the javascript code that represents a table
    :param df: a Pandas data frame
    :param classes: classes for the html table, see https://datatables.net/manual/styling/classes
    :param html_id: a unique identifier for the table
    :param show_index: 'auto' (show the index unless it is an unnamed Range Index), True or False
    :param max_bytes: the largest memory size for which we wish to display the dataframe.
    """
    if isinstance(df, (np.ndarray, np.generic)):
        df = pd.DataFrame(df)

    if isinstance(df, pd.Series):
        df = df.to_frame()

    if df.values.nbytes > max_bytes > 0:
        raise ValueError('The dataframe has size {}, larger than the limit {}'.format(df.values.nbytes, max_bytes) +
                         '\nPlease print a smaller dataframe, or print it with a larger/no limit with '
                         'show(df, max_bytes=0)')

    html_id = html_id or str(uuid.uuid4())
    if isinstance(classes, list):
        classes = ' '.join(classes)

    if show_index == 'auto':
        show_index = df.index.name is not None or not isinstance(df.index, pd.RangeIndex)

    if not show_index:
        df = df.set_index(pd.RangeIndex(len(df.index)))

    # Generate table head using pandas.to_html()
    pattern = re.compile(r'.*<thead>(.*)</thead>', flags=re.MULTILINE | re.DOTALL)
    match = pattern.match(df.head(0).to_html())
    thead = match.groups()[0]
    if not show_index:
        thead = thead.replace('<th></th>', '', 1)
    html_table = '<table id="' + html_id + '" class="' + classes + '"><thead>' + thead + '</thead></table>'

    # Table content as 'data' for DataTable
    formatted_df = df.reset_index() if show_index else df.copy()
    for col in formatted_df:
        x = formatted_df[col]
        if x.dtype.kind in ['b', 'i', 's']:
            continue

        if x.dtype.kind == 'O':
            formatted_df[col] = formatted_df[col].astype(unicode)
            continue

        formatted_values = np.array(fmt.format_array(x.values, None))
        if x.dtype.kind == 'f':
            formatted_df[col] = formatted_values.astype(np.float)
        else:
            formatted_df[col] = formatted_values

    kwargs['data'] = formatted_df.values.tolist()
    try:
        dt_args = json.dumps(kwargs)
        return """$(element).html(`""" + html_table + """`);

require(["datatables"], function (datatables) {
    $(document).ready(function () {
        table = $('#""" + html_id + """').DataTable(""" + dt_args + """);
    });
})"""
    except TypeError as error:
        warnings.warn(str(error))
        return ''


def show(df=None, **kwargs):
    """Show a dataframe"""
    script = datatables(df, **kwargs)
    display(Javascript(script))


def init_itable_mode():
    """Activate the representation of Pandas dataframes as interactive tables"""
    pd.DataFrame._repr_javascript_ = datatables
    pd.Series._repr_javascript_ = datatables
