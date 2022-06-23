// Setup - add a text input to each header or footer cell
$('#table_id thead_or_tfoot th').each(function () {
    let title = $(this).text();
    $(this).html('<input type="text" placeholder="Search ' +
        // We use encodeURI to avoid this LGTM error:
        // https://lgtm.com/rules/1511866576920/
        encodeURI(title).replaceAll("%20", " ") +
        '" />');
});
