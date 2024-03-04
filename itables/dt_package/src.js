import JSZip from 'jszip';
import jQuery from 'jquery';
import DataTable from 'datatables.net-dt';
import 'datatables.net-dt/css/dataTables.dataTables.min.css';

import 'datatables.net-buttons';
import 'datatables.net-buttons/js/buttons.html5.mjs';
import 'datatables.net-buttons/js/buttons.print.mjs';
import 'datatables.net-buttons-dt/css/buttons.dataTables.min.css';

DataTable.Buttons.jszip(JSZip);

export { DataTable, jQuery };
