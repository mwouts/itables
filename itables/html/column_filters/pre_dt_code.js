// Setup - add a text input to each footer cell
$('#table_id thead th').each(function () {
        var title = $(this).text();
        $(this).html('<input type="text" placeholder="Search ' + title + '" />');
});
