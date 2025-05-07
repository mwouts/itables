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

DataTable.parseJSON = function (jsonString) {
    return JSON.parse(jsonString, (key, value, context) => {
        // At this stage, BigInts have been parsed as numbers already. Consequently, if the value appears
        // to be a number that should be a BigInt, we re-evaluate it from the original string.
        if (typeof value === 'number' && !Number.isSafeInteger(value) && /^-?\d+$/.test(context.source)) {
            return BigInt(context.source);
        }
        if (value === "___NaN___") return NaN;
        if (value === "___Infinity___") return Infinity;
        if (value === "___-Infinity___") return -Infinity;
        return value;
    });
}

function textInHeaderCanBeSelected(settings, json) {
    // Get the Datables API
    let api = this.api();

    // Iterate over all the thead > th elements
    jQuery('thead th', api.table().container()).each(function () {
        if (jQuery(this).attr("colSpan") > 1) {
            // No sorting on complex headers
            // (but keep the icon for alignment)
            jQuery(this).attr('data-dt-order', 'disable');
        }
        else if (jQuery(this).text().trim() === '') {
            // Remove the sorting icon on empty cells
            jQuery(this).empty();
            jQuery(this).attr('data-dt-order', 'disable');
        }
        else {
            // Apply the icon-only data-dt-order attribute
            jQuery(this).attr('data-dt-order', 'icon-only');

            // get the current column index
            let colIndex = api.column(this).index('visible');

            // Apply the order listener to the order icon
            api.order.listener(jQuery('span.dt-column-order', this), colIndex);
        }
    });
};

DataTable.updateInitComplete = function (dt_args) {
if (dt_args['text_in_header_can_be_selected'] === true) {
    if (dt_args['initComplete'] === undefined) {
        dt_args['initComplete'] = textInHeaderCanBeSelected;
    } else {
        const oldInitComplete = dt_args['initComplete'];
        dt_args['initComplete'] = function(settings, json) {
            textInHeaderCanBeSelected(settings, json);
            oldInitComplete(settings, json);
        };
    }
}
delete dt_args['text_in_header_can_be_selected'];
};

DataTable.adjust_theme = function () {
    let is_dark_theme = function () {
        // Jupyter Lab
        if ('jpThemeLight' in document.body.dataset)
            return (document.body.dataset.jpThemeLight === "false");

        // VS Code
        if ('vscodeThemeKind' in document.body.dataset)
            return document.body.dataset.vscodeThemeKind.includes('dark');

        // Jupyter Book
        if ('theme' in document.documentElement.dataset)
            return document.documentElement.dataset.theme.includes('dark');

        // Default
        return window.matchMedia('(prefers-color-scheme: dark)').matches;
    }

    if (is_dark_theme()) {
        document.documentElement.classList.add('dark');
    }
    else {
        document.documentElement.classList.remove('dark');
    }
}

export { DataTable, DateTime, jQuery };

export default DataTable;
