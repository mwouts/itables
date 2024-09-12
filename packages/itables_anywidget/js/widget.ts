import type { RenderContext } from "@anywidget/types";

// DataTable and its css
import DataTable from 'dt_for_itables';
import 'dt_for_itables/dt_bundle.css';

/* Specifies attributes defined with traitlets in ../src/itables_anywidget/__init__.py */
interface WidgetModel {
	dt_args: object;
	other_args: object;
}

function render({ model, el }: RenderContext<WidgetModel>) {
	let table = document.createElement("table");
	el.classList.add("itables_anywidget");
	el.appendChild(table);

	let dt_args = model.get('dt_args');
	let other_args = model.get('other_args');

	table.setAttribute('class', other_args.classes);
	table.setAttribute('style', other_args.style);

	if (other_args.caption) {
		let caption = table.createCaption();
		caption.textContent = other_args.caption;
	}

	if (other_args.downsampling_warning) {
		dt_args["fnInfoCallback"] = function (oSettings: any, iStart: number, iEnd: number, iMax: number, iTotal: number, sPre: string) {
			return sPre + ' (' +
				other_args.downsampling_warning + ')'
		}
	}

	new DataTable(table, dt_args);
}

export default { render };
