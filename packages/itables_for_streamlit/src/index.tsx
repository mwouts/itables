import { Streamlit, RenderData } from "streamlit-component-lib"

import DataTable from "dt_for_itables"
import "dt_for_itables/dt_bundle.css"

// Create a table element
const span = document.body.appendChild(document.createElement("span"))
const table = span.appendChild(document.createElement("table"))
let dt = new DataTable(table)

function onRender(event: Event): void {
  // dt_args is the whole map of arguments passed on the Python side
  var other_args = (event as CustomEvent<RenderData>).detail.args.other_args
  var dt_args = (event as CustomEvent<RenderData>).detail.args.dt_args

  if(other_args.downsampling_warning) {
    dt_args["fnInfoCallback"] = function (oSettings:any, iStart:number, iEnd:number, iMax:number, iTotal:number, sPre:string) { return sPre + ' (' +
    other_args.downsampling_warning + ')' }
  }

  // As we can't pass the dt_args other than in the
  // DataTable constructor, we call
  // destroy and then re-create the table
  dt.destroy()

  // Set the class and style here otherwise the width
  // might become a fixed width
  table.setAttribute('class', other_args.classes)
  table.setAttribute('style', other_args.style)

  dt = new DataTable(table, dt_args)
  if(other_args.caption) {
    dt.caption(other_args.caption)
  }

  function export_selected_rows() {
		let selected_rows:Array<number> = Array.from(dt.rows({ selected: true }).indexes());

    let full_row_count:number = other_args.full_row_count;
		let data_row_count:number = dt_args.data.length;

    // Here the selected rows are for the datatable.
		// We convert them back to the full table
		if (data_row_count < full_row_count) {
			let bottom_half = data_row_count / 2;
			selected_rows = selected_rows.map(
				(x:number, i:number) => (x < bottom_half ? x : x + full_row_count - data_row_count));
		}

    Streamlit.setComponentValue({selected_rows});
	};

	dt.on('select', function (e: any, dt: any, type: any, indexes: any) {
		export_selected_rows();
	});

	dt.on('deselect', function (e: any, dt: any, type: any, indexes: any) {
		export_selected_rows();
	});

  // we recalculate the height
  Streamlit.setFrameHeight()
}

// connect the render function to Streamlit
Streamlit.events.addEventListener(Streamlit.RENDER_EVENT, onRender)
Streamlit.setComponentReady()
