require.config({
    paths: {
        // 'require' and 'jquery' need to be explicitly required for JupyterLab
        // https://github.com/mwouts/itables/issues/3#issuecomment-688330386
        require: 'https://cdnjs.cloudflare.com/ajax/libs/require.js/2.1.10/require.min',
        jquery: 'https://cdnjs.cloudflare.com/ajax/libs/jquery/2.0.3/jquery.min',
        datatables: 'https://cdn.datatables.net/1.10.19/js/jquery.dataTables.min',
    }
});

$('head').append('<link rel="stylesheet" type="text/css" \
                href = "https://cdn.datatables.net/1.10.19/css/jquery.dataTables.min.css" > ');

$('head').append('<style> table td { text-overflow: ellipsis; overflow: hidden; } </style>');
