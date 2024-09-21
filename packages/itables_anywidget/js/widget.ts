import type { RenderContext } from "@anywidget/types";

// DataTable and its css
import { DataTable, jQuery } from 'dt_for_itables';
import 'dt_for_itables/dt_bundle.css';

/* Specifies attributes defined with traitlets in ../src/itables_anywidget/__init__.py */
interface WidgetModel {
	dt_args: object;
	caption: string;
	classes: string;
	style: string;
	downsampling_warning: string;
	selected_rows: Array<number>;
}

function render({ model, el }: RenderContext<WidgetModel>) {
	let table = document.createElement("table");
	el.classList.add("itables_anywidget");
	el.appendChild(table);

	function update_classes() {
		table.setAttribute('class', model.get("classes"));
	}
	function update_style() {
		table.setAttribute('style', model.get("style"));
	}
	function update_caption() {
		let caption_text = model.get('caption');
		if (caption_text) {
			let caption = table.createCaption();
			caption.textContent = caption_text;
		} else { table.deleteCaption() };
	}

	// Set initial values
	update_classes();
	update_style();
	update_caption();

	// Update the table when one of these change
	model.on("change:classes", update_classes);
	model.on("change:style", update_style);
	model.on("change:caption", update_caption);

	// This variable is a place holder from the
	// DataTable instance. This way we can re-create it
	// from within 'create_table'
	let dt = null;

	let setting_selected_rows_from_model = false;
	function set_selected_rows_from_model() {
		// We use this variable to avoid triggering model updates!
		setting_selected_rows_from_model = true;

		// The model selected rows are for the full table, so
		// we map them to the actual data
		let selected_rows = model.get('selected_rows');
		let full_row_count = model.get('full_row_count');
		let data_row_count = model.get('data').length;
		let bottom_half = data_row_count / 2;
		let top_half = full_row_count - bottom_half;
		selected_rows = Array.from(selected_rows.filter(i => i >= 0 && i < full_row_count && (i < bottom_half || i >= top_half)).map(
			i => (i < bottom_half) ? i : i - full_row_count + data_row_count));
		dt.rows().deselect();
		dt.rows(selected_rows).select();

		setting_selected_rows_from_model = false;
	};

	function create_table(destroy = false) {
		let dt_args = model.get('dt_args');
		if (destroy) {
			dt.destroy();
			jQuery(table).empty();
		}

		dt_args["fnInfoCallback"] = function (oSettings: any, iStart: number, iEnd: number, iMax: number, iTotal: number, sPre: string) {
			let msg = model.get("downsampling_warning");
			if (msg)
				return sPre + ' (' + model.get("downsampling_warning") + ')';
			else
				return sPre;
		}
		dt_args['data'] = model.get('data');
		dt = new DataTable(table, dt_args);
	}
	create_table();
	set_selected_rows_from_model();

	model.on('change:destroy_and_recreate', () => {
		create_table(true);
	});

	model.on("change:selected_rows", set_selected_rows_from_model);

	function export_selected_rows() {
		if (setting_selected_rows_from_model)
			return;

		let selected_rows = Array.from(dt.rows({ selected: true }).indexes());

		// Here the selected rows are for the datatable.
		// We convert them back to the full table
		let full_row_count = model.get('full_row_count');
		let data_row_count = model.get('data').length;
		let bottom_half = data_row_count / 2;
		selected_rows = Array.from(selected_rows.map(
			i => (i < bottom_half ? i : i + full_row_count - data_row_count)));

		model.set('selected_rows', selected_rows);
		model.save_changes();
	};

	dt.on('select', function (e: any, dt: any, type: any, indexes: any) {
		export_selected_rows();
	});

	dt.on('deselect', function (e: any, dt: any, type: any, indexes: any) {
		export_selected_rows();
	});
}

export default { render };
