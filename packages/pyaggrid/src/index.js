import {
    AllCommunityModule,
    createGrid,
    ModuleRegistry,
    themeAlpine,
    themeBalham,
    themeMaterial,
    themeQuartz,
} from 'ag-grid-community';

ModuleRegistry.registerModules([AllCommunityModule]);

// AG Grid draws a header column separator and a resize handle after every
// column, including the last one, which clashes with the grid's own outer
// border.
if (!document.getElementById('pyaggrid-header-border-fix')) {
    const style = document.createElement('style');
    style.id = 'pyaggrid-header-border-fix';
    style.textContent = '.ag-header-cell:last-of-type::after{border-right:none;border-left:none;}'
        + '.ag-header-cell:last-of-type .ag-header-cell-resize{display:none;}';
    document.head.appendChild(style);
}

const themes = {
    quartz: themeQuartz,
    balham: themeBalham,
    material: themeMaterial,
    alpine: themeAlpine,
};

// itables sentinels -> null/Infinity
function fixValue(v) {
    return v === "___NaN___" ? null
        : v === "___Infinity___" ? Infinity
            : v === "___-Infinity___" ? -Infinity
                : v;
}

function evalNestedKeys(obj, keys, context) {
    const [first, ...rest] = keys;
    if (rest.length === 0) {
        try {
            obj[first] = eval?.("(" + obj[first] + ")");
        }
        catch (e) {
            console.error(`Error evaluating ${context}='${obj[first]}': ${e.message}`);
        }
    }
    else {
        evalNestedKeys(obj[first], rest, context);
    }
}

function syncPyaggridSiblingWidths(container) {
    let sibling = container.nextElementSibling;
    while (sibling && sibling.className.startsWith('pyaggrid-')) {
        sibling.style.width = container.style.width;
        sibling = sibling.nextElementSibling;
    }
}

/**
 * A thin wrapper around an AG Grid instance, that renders the
 * grid_args prepared by the pyaggrid Python package, and exposes
 * the selected rows (by their index in the original dataframe).
 */
class AgGridTable {
    constructor(container, grid_args) {
        const { data_json, grid_options, downsampling_warning, ...rest } = grid_args;
        const gridOptions = { ...(grid_options || {}) };

        // Evaluate the JavascriptCode and JavascriptFunction values
        (gridOptions.keys_to_be_evaluated || []).forEach(keys =>
            evalNestedKeys(gridOptions, keys, keys.join('.')));
        delete gridOptions.keys_to_be_evaluated;

        if (typeof gridOptions.theme === 'string')
            gridOptions.theme = themes[gridOptions.theme] || themeQuartz;

        if (gridOptions.themeParams) {
            gridOptions.theme = gridOptions.theme.withParams(gridOptions.themeParams);
            delete gridOptions.themeParams;
        }

        if (gridOptions.rowData === undefined) {
            // row arrays -> objects keyed c0..cN, plus the original row index
            const data = JSON.parse(data_json || '[]');
            gridOptions.rowData = data.map((row, i) => {
                const obj = Object.fromEntries(row.map((v, j) => ['c' + j, fixValue(v)]));
                obj.__row = i;
                return obj;
            });
        }

        // Selection events
        this._suppressSelectionEvents = false;
        this._selectionCallbacks = [];
        const userSelectionChanged = gridOptions.onSelectionChanged;
        gridOptions.onSelectionChanged = (params) => {
            if (userSelectionChanged) userSelectionChanged(params);
            if (!this._suppressSelectionEvents)
                this._selectionCallbacks.forEach(cb => cb());
        };

        // Resize and layout the grid after data is rendered, so that
        // the grid container is not bigger than the table content.
        // Skip for domLayout:'normal' where the user controls container size.
        if (gridOptions.domLayout !== 'normal') {
            const userCallback = gridOptions.onFirstDataRendered;
            gridOptions.onFirstDataRendered = (params) => {
                if (userCallback) userCallback(params);

                // autoSizeAllColumns() runs synchronously here, so column widths
                // are final before we measure them below.
                if (gridOptions.autoSizeStrategy === undefined) {
                    params.api.autoSizeAllColumns();
                }

                const cols = params.api.getColumns();
                if (!cols || cols.length === 0) return;

                const totalColWidth = cols.reduce((sum, col) => sum + col.getActualWidth(), 0);
                const parentWidth = container.parentElement ? container.parentElement.offsetWidth : Infinity;

                // Shrink the div to column width first; this forces the browser to reflow
                // so that pagingPanel.scrollWidth reflects the pagination bar's natural
                // minimum width rather than its stretched 100%-parent width.
                container.style.width = Math.min(totalColWidth + 2, parentWidth) + 'px';
                const pagingPanel = container.querySelector('.ag-paging-panel');
                // The paging panel wraps onto multiple lines (flex-wrap: wrap-reverse)
                // once it no longer fits on one line; force it back to a single line
                // while measuring, or scrollWidth would report the already-wrapped
                // (smaller) width instead of the panel's true minimum width.
                let paginationMinWidth = 0;
                if (pagingPanel) {
                    const previousFlexWrap = pagingPanel.style.flexWrap;
                    pagingPanel.style.flexWrap = 'nowrap';
                    paginationMinWidth = pagingPanel.scrollWidth;
                    pagingPanel.style.flexWrap = previousFlexWrap;
                }
                const contentWidth = Math.max(totalColWidth, paginationMinWidth);
                container.style.width = Math.min(contentWidth + 2, parentWidth) + 'px';

                // Keep framework-rendered caption and warning blocks aligned with
                // the measured grid width, matching the standalone HTML renderer.
                syncPyaggridSiblingWidths(container);

                // Centre the header row and data rows within the div when the
                // pagination bar is wider than the column area.
                if (paginationMinWidth > totalColWidth) {
                    const colOffset = Math.floor((contentWidth - totalColWidth) / 2);
                    const headerRow = container.querySelector('.ag-header-row');
                    const colContainer = container.querySelector('.ag-center-cols-container');
                    if (headerRow) headerRow.style.left = colOffset + 'px';
                    if (colContainer) colContainer.style.marginLeft = colOffset + 'px';
                }

                // Hide the horizontal scroll track (eliminates blank space below rows)
                // when there is no horizontal overflow.
                if (totalColWidth + 2 <= contentWidth + 2) {
                    params.api.setGridOption('suppressHorizontalScroll', true);
                }
            };
        }

        this.api = createGrid(container, gridOptions);
    }

    get selected_rows() {
        const rows = [];
        this.api.forEachNode(node => {
            if (node.isSelected()) rows.push(node.data.__row);
        });
        return rows.sort((a, b) => a - b);
    }

    set selected_rows(rows) {
        const selection = new Set(rows || []);
        this._suppressSelectionEvents = true;
        this.api.forEachNode(node => {
            node.setSelected(selection.has(node.data.__row));
        });
        this._suppressSelectionEvents = false;
    }

    onSelectionChanged(callback) {
        this._selectionCallbacks.push(callback);
    }

    destroy() {
        this.api.destroy();
    }
}

export { AgGridTable, themes };
export default AgGridTable;
