require.config({
    paths: {
        jquery: 'https://code.jquery.com/jquery-3.5.1.min',
        datatables: 'https://cdn.datatables.net/1.11.3/js/jquery.dataTables.min',
    }
});

require(['jquery'], function($) {
    $('head').append('<link rel="stylesheet" type="text/css" \
                href = "https://cdn.datatables.net/1.10.19/css/jquery.dataTables.min.css" > ');
    $('head').append('<style> table td { text-overflow: ellipsis; overflow: hidden; } </style>');
});
