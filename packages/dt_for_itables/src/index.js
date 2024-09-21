import JSZip from 'jszip';
import jQuery from 'jquery';
import DataTable from 'datatables.net-dt';
import 'datatables.net-dt/css/dataTables.dataTables.min.css';

import 'datatables.net-buttons-dt';
import 'datatables.net-buttons/js/buttons.html5.min.mjs';
import 'datatables.net-buttons/js/buttons.print.min.mjs';
import 'datatables.net-buttons/js/buttons.colVis.min.mjs';
import 'datatables.net-buttons-dt/css/buttons.dataTables.min.css';

DataTable.Buttons.jszip(JSZip);

import 'datatables.net-fixedcolumns-dt';
import 'datatables.net-fixedcolumns-dt/css/fixedColumns.dataTables.min.css';

import 'datatables.net-keytable-dt';
import 'datatables.net-keytable-dt/css/keyTable.dataTables.min.css';

import 'datatables.net-rowgroup-dt';
import 'datatables.net-rowgroup-dt/css/rowGroup.dataTables.min.css';

import DateTime from 'datatables.net-datetime';
import 'datatables.net-datetime/dist/dataTables.dateTime.min.css';

import 'datatables.net-searchbuilder-dt';
import 'datatables.net-searchbuilder-dt/css/searchBuilder.dataTables.min.css';

import 'datatables.net-searchpanes-dt';
import 'datatables.net-searchpanes-dt/css/searchPanes.dataTables.min.css';

import 'datatables.net-select-dt';
import 'datatables.net-select-dt/css/select.dataTables.min.css';

import './index.css';

DataTable.get_selected_rows = function (dt, filtered_row_count) {
    // Here the selected rows are for the datatable.
    // We convert them back to the full table
    let data_row_count = dt.rows().count();
    let bottom_half = data_row_count / 2;
    return Array.from(dt.rows({ selected: true }).indexes().map(
        i => (i < bottom_half ? i : i + filtered_row_count)));
}

DataTable.set_selected_rows = function (dt, filtered_row_count, selected_rows) {
    let data_row_count = dt.rows().count();
    let bottom_half = data_row_count / 2;
    let top_half = bottom_half + filtered_row_count;
    let full_row_count = data_row_count + filtered_row_count;
    selected_rows = Array.from(selected_rows.filter(i => i >= 0 && i < full_row_count && (i < bottom_half || i >= top_half)).map(
        i => (i < bottom_half) ? i : i - filtered_row_count));
    dt.rows().deselect();
    dt.rows(selected_rows).select();
}

export { DataTable, DateTime, jQuery };

export default DataTable;
