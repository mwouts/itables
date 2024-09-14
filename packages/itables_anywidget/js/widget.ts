import type { RenderContext } from "@anywidget/types";

// DataTable and its css
import DataTable from 'dt_for_itables';
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

	let dt_args = model.get('dt_args');
	if (model.get("downsampling_warning")) {
		dt_args["fnInfoCallback"] = function (oSettings: any, iStart: number, iEnd: number, iMax: number, iTotal: number, sPre: string) {
			return sPre + ' (' +
				model.get("downsampling_warning") + ')'
		}
	}
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
	update_classes();
	update_style();
	update_caption();

	let dt = new DataTable(table, dt_args);

	// Set the initial selected rows (not a callback on model otherwise
	// we run into infinite loops, not sure how to avoid that?)
	model.get('selected_rows').forEach(idx => {
		dt.row(idx).select()
	});

	// Update the table when one of these change
	model.on("change:classes", update_classes);
	model.on("change:style", update_style);
	model.on("change:caption", update_caption);

	function export_selected_rows() {
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
