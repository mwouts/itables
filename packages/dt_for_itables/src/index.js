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

function parseJSON(jsonString) {
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

// The global eval in evalNestedKeys might need jQuery
window.$ = jQuery;

function evalNestedKeys(obj, keys, context) {
    const [first, ...rest] = keys;
    if (['__proto__', 'constructor', 'prototype'].includes(first)) {
        throw new Error(`Invalid key '${first}' in context '${context}'. Prototype pollution attempt detected.`);
    }
    if (rest.length === 0) {
        try {
            let code = obj[first];
            if (typeof code !== 'string') {
                throw new Error(`Expected a string to evaluate in context '${context}', but got ${typeof code}.`);
            }
            if (/^\s*function\s*\(/.test(code)) {
                // If the code matches the regular expression for a function definition,
                // we wrap it in parentheses to proceed with the evaluation.
                code = `(${code})`;
            }

            obj[first] = window.eval(code);
        }
        catch (e) {
            console.error(`Error evaluating ${context}='${obj[first]}'": ${e.message}`);
        }
    }
    else {
        evalNestedKeys(obj[first], rest, context);
    }
}

class ITable {
    constructor(table, itable_args) {
        const { data, caption, classes, style, data_json, table_html, table_style, selected_rows, filtered_row_count, keys_to_be_evaluated, column_filters, text_in_header_can_be_selected, initComplete, downsampling_warning, render_math = false, ...dt_args } = itable_args;
        if (data !== undefined) {
            throw new Error("The 'data' property is not allowed in dt_args.");
        }
        if (data_json) {
            dt_args.data = parseJSON(data_json);
        }
        if (keys_to_be_evaluated) {
            keys_to_be_evaluated.forEach(keys => evalNestedKeys(dt_args, keys, keys.join('.')));
        }

        this.filtered_row_count = filtered_row_count || 0;

        if (render_math) {
            // Add drawCallback for math rendering
            const originalDrawCallback = dt_args.drawCallback;
            dt_args.drawCallback = (settings) => {
                // Call original drawCallback if it exists
                if (originalDrawCallback) {
                    originalDrawCallback.call(this.dt, settings);
                }

                console.log("Processing math in visible cells...");
                let MathJax = window.MathJax;
                // Ensure MathJax is loaded
                if (typeof MathJax === 'undefined') {
                    console.error("MathJax is not loaded. Please ensure MathJax is included in your project.");
                    return;
                }

                // Process math in the visible cells
                jQuery(settings.nTable).find('tbody td').each((i, cell) => {
                    const content = jQuery(cell).html();
                    if (content && content.includes('$')) {

                        // Check which version of MathJax is available
                        if (typeof MathJax !== 'undefined') {
                            if (MathJax.version && MathJax.version[0] === '3') {
                                // MathJax v3 API
                                try {
                                    console.log("Starting MathJax typesetting for cell...");
                                    MathJax.typesetPromise([cell])
                                        .then(() => console.log("MathJax typesetting completed for cell", cell))
                                        .catch(err => console.error("MathJax typesetting failed:", err));
                                } catch (e) {
                                    console.error("Error using MathJax v3:", e);
                                }
                            }
                        } else {
                            // MathJax v2 API
                            try {
                                MathJax.Hub.Queue(["Typeset", MathJax.Hub, cell]);
                            } catch (e) {
                                console.error("Error using MathJax v2:", e);
                            }
                        }
                    }
                });
            }
        }

        if (text_in_header_can_be_selected || column_filters) {
            dt_args.initComplete = function (settings, json) {
                if (column_filters == 'header') {
                    this.api()
                        .columns()
                        .every(function () {
                            const that = this;

                            jQuery('input', this.header()).on('keyup change clear', function () {
                                if (that.search() !== this.value) {
                                    that.search(this.value).draw();
                                }
                            });
                        });
                } else if (column_filters == 'footer') {
                    this.api()
                        .columns()
                        .every(function () {
                            const that = this;

                            jQuery('input', this.footer()).on('keyup change clear', function () {
                                if (that.search() !== this.value) {
                                    that.search(this.value).draw();
                                }
                            });
                        });
                }
                if (text_in_header_can_be_selected) {
                    // Get the Datables API
                    let api = this.api();

                    // Iterate over all the thead > th elements
                    jQuery('thead th', api.table().container()).each(function () {
                        if (jQuery(this).attr("colSpan") > 1) {
                            // No sorting on complex headers
                            // (but keep the icon for alignment)
                            jQuery(this).attr('data-dt-order', 'disable');
                        }
                        else if (jQuery(this).find('span.dt-column-title').text() === '' && jQuery(this).find('span.dt-column-title').children().length === 0) {
                            // Remove the sorting icon on empty headers
                            jQuery(this).attr('data-dt-order', 'disable');
                            jQuery(this).empty();
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
                }
                if (initComplete !== undefined)
                    initComplete(settings, json);
            }
        }

        if (downsampling_warning) {
            dt_args["fnInfoCallback"] = function (oSettings, iStart, iEnd, iMax, iTotal, sPre) {
                return sPre + ' (' + downsampling_warning + ')';
            }
        }

        this.table = jQuery(table);
        if (table_html) {
            this.table.html(table_html);
        }
        if (classes) {
            classes.forEach(element => {
                this.table.addClass(element);
            });
        }
        if (style) {
            this.table.css(style);
        }
        if (table_style) {
            $('<style id="' + this.table.attr('id') + '-style">')
                .text(table_style)
                .appendTo(this.table);
        }
        if (column_filters === "header" || column_filters === "footer") {
            let thead_or_tfoot = (column_filters === "header") ? "thead" : "tfoot";
            this.table.find(thead_or_tfoot + ' th').each(function () {
                let input = document.createElement("input");
                input.type = "text";
                input.placeholder = jQuery(this).text();

                jQuery(this).html(input);
            });
        }
        this.dt = new DataTable(table, dt_args);
        if (caption !== undefined) {
            this.dt.caption(caption);
        }
        if (selected_rows !== undefined) {
            this.selected_rows = selected_rows;
        }
    }

    destroy() {
        if (this.dt) {
            this.dt.destroy();
            this.table.empty();
            this.dt = null;
        }
    }

    set selected_rows(selected_rows) {
        let data_row_count = this.dt.rows().count();
        let bottom_half = data_row_count / 2;
        let top_half = bottom_half + this.filtered_row_count;
        let full_row_count = data_row_count + this.filtered_row_count;
        selected_rows = Array.from(selected_rows.filter(i => i >= 0 && i < full_row_count && (i < bottom_half || i >= top_half)).map(
            i => (i < bottom_half) ? i : i - this.filtered_row_count));
        this.dt.rows().deselect();
        this.dt.rows(selected_rows).select();
    }

    get selected_rows() {
        // Here the selected rows are for the datatable.
        // We convert them back to the full table
        let data_row_count = this.dt.rows().count();
        let bottom_half = data_row_count / 2;
        return Array.from(this.dt.rows({ selected: true }).indexes().map(
            i => (i < bottom_half ? i : i + this.filtered_row_count)));
    }
}

function set_or_remove_dark_class() {
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

export { ITable, DateTime, jQuery, set_or_remove_dark_class };

export default DataTable;
