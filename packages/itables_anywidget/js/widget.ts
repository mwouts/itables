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
		table.setAttribute('classes', model.get("classes"));
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

	function update_data() {
		dt.clear().draw();
		model.get('data').forEach(row => {
			dt.row.add(row).draw(false);
		});
		set_selected_rows_from_model();
	}

	let setting_selected_rows_from_model = false;
	function set_selected_rows_from_model() {
		// We use this variable to avoid triggering model updates!
		setting_selected_rows_from_model = true;
		dt.rows().deselect();
		dt.rows(model.get('selected_rows')).select();
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
		dt = new DataTable(table, dt_args);
		update_data();
	}
	create_table();

	model.on('change:dt_args', () => {
		create_table(true);
	});

	model.on("change:data", update_data);
	model.on("change:selected_rows", set_selected_rows_from_model);

	function export_selected_rows() {
		if (setting_selected_rows_from_model)
			return;

		let selected_rows = Array.from(dt.rows({ selected: true }).indexes());
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
