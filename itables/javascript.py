import re
import uuid
import json
import pandas as pd
import numpy as np
import pandas.io.formats.format as fmt
import warnings
from IPython.core.display import display, Javascript, HTML
import itables.options as opt

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


def _datatables_repr_(df=None, tableId=None, **kwargs):
    """Return the HTML/javascript representation of the table"""

    # Default options
    for option in dir(opt):
        if not option in kwargs and not option.startswith("__"):
            kwargs[option] = getattr(opt, option)

    # These options are used here, not in DataTable
    classes = kwargs.pop('classes')
    showIndex = kwargs.pop('showIndex')
    maxBytes = kwargs.pop('maxBytes')

    if isinstance(df, (np.ndarray, np.generic)):
        df = pd.DataFrame(df)

    if isinstance(df, pd.Series):
        df = df.to_frame()

    if df.values.nbytes > maxBytes > 0:
        raise ValueError('The dataframe has size {}, larger than the limit {}\n'.format(df.values.nbytes, maxBytes) +
                         'Please print a smaller dataframe, or enlarge or remove the limit:\n'
                         'import itables.options as opt; opt.maxBytes=0')

    # Do not show the page menu when the table has fewer rows than min length menu
    if 'paging' not in kwargs and len(df.index) <= kwargs.get('lengthMenu', [10])[0]:
        kwargs['paging'] = False

    tableId = tableId or str(uuid.uuid4())
    if isinstance(classes, list):
        classes = ' '.join(classes)

    if showIndex == 'auto':
        showIndex = df.index.name is not None or not isinstance(df.index, pd.RangeIndex)

    if not showIndex:
        df = df.set_index(pd.RangeIndex(len(df.index)))

    # Generate table head using pandas.to_html()
    pattern = re.compile(r'.*<thead>(.*)</thead>', flags=re.MULTILINE | re.DOTALL)
    match = pattern.match(df.head(0).to_html())
    thead = match.groups()[0]
    if not showIndex:
        thead = thead.replace('<th></th>', '', 1)
    html_table = '<table id="' + tableId + '" class="' + classes + '"><thead>' + thead + '</thead></table>'

    # Table content as 'data' for DataTable
    formatted_df = df.reset_index() if showIndex else df.copy()
    for col in formatted_df:
        x = formatted_df[col]
        if x.dtype.kind in ['b', 'i', 's']:
            continue

        if x.dtype.kind == 'O':
            formatted_df[col] = formatted_df[col].astype(unicode)
            continue

        formatted_df[col] = np.array(fmt.format_array(x.values, None))
        if x.dtype.kind == 'f':
            try:
                formatted_df[col] = formatted_df[col].astype(np.float)
            except ValueError:
                pass

    kwargs['data'] = formatted_df.values.tolist()

    try:
        dt_args = json.dumps(kwargs)
        return """<div>""" + html_table + """
<script type="text/javascript">
require(["datatables"], function (datatables) {
    $(document).ready(function () {
        var dt_args = """ + dt_args + """;        
        table = $('#""" + tableId + """').DataTable(dt_args);
    });
})
</script>
</div>
"""
    except TypeError as error:
        warnings.warn(str(error))
        return ''


def show(df=None, **kwargs):
    """Show a dataframe"""
    html = _datatables_repr_(df, **kwargs)
    display(HTML(html))
