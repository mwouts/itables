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
		DataTable.set_selected_rows(dt, model.get('_filtered_row_count'), model.get('selected_rows'));
		setting_selected_rows_from_model = false;
	};

	function create_table(destroy = false) {
		if (destroy) {
			dt.destroy();
			jQuery(table).empty();
		}

		let dt_args = model.get('_dt_args');
		dt_args['data'] = model.get('_data');
		dt_args['columns'] = model.get('_columns');
		dt_args["fnInfoCallback"] = function (oSettings: any, iStart: number, iEnd: number, iMax: number, iTotal: number, sPre: string) {
			let msg = model.get("_downsampling_warning");
			if (msg)
				return sPre + ' (' + msg + ')';
			else
				return sPre;
		}
		dt = new DataTable(table, dt_args);
		set_selected_rows_from_model();
	}
	create_table();

	model.on('change:_destroy_and_recreate', () => {
		create_table(true);
	});

	model.on("change:selected_rows", set_selected_rows_from_model);

	function export_selected_rows() {
		if (setting_selected_rows_from_model)
			return;

		model.set('selected_rows', DataTable.get_selected_rows(dt, model.get('_filtered_row_count')));
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
