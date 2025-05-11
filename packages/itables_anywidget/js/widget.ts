import type { RenderContext } from "@anywidget/types";

// DataTable and its css
import { ITable, set_or_remove_dark_class } from 'dt_for_itables';
import 'dt_for_itables/dt_bundle.css';

/* Specifies attributes defined with traitlets in ../src/itables_anywidget/__init__.py */
interface WidgetModel {
	dt_args: object;
	caption: string;
	classes: string;
	style: string;
}

function render({ model, el }: RenderContext<WidgetModel>) {
	set_or_remove_dark_class();
	let table = document.createElement("table");
	el.classList.add("itables_anywidget");
	el.appendChild(table);

	function update_classes() {
		table.className = model.get("classes");
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
		dt.selected_rows = model.get('selected_rows');
		setting_selected_rows_from_model = false;
	};

	function update_table() {
		if (dt) {
			dt.destroy();
		}

		let dt_args = model.get('_dt_args');
		dt = new ITable(table, dt_args);
		set_selected_rows_from_model();
	}
	update_table();

	model.on('change:_dt_args', () => {
		update_table();
	});

	model.on("change:selected_rows", set_selected_rows_from_model);

	function export_selected_rows() {
		if (setting_selected_rows_from_model)
			return;

		model.set('selected_rows', dt.selected_rows);
		model.save_changes();
	};

	dt.dt.on('select', function (e: any, dt: any, type: any, indexes: any) {
		export_selected_rows();
	});

	dt.dt.on('deselect', function (e: any, dt: any, type: any, indexes: any) {
		export_selected_rows();
	});
}

export default { render };
