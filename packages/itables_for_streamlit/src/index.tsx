import { Streamlit, RenderData } from "streamlit-component-lib"

import {ITable, set_or_remove_dark_class} from "dt_for_itables"
import "dt_for_itables/dt_bundle.css"

set_or_remove_dark_class();
// Create a table element
const span = document.body.appendChild(document.createElement("span"))
const table = span.appendChild(document.createElement("table"))
let dt = new ITable(table, {})

function onRender(event: Event): void {
  // dt_args is the whole map of arguments passed on the Python side
  var other_args = (event as CustomEvent<RenderData>).detail.args.other_args;
  const dt_args = (event as CustomEvent<RenderData>).detail.args.dt_args;

  // As we can't pass the dt_args other than in the
  // DataTable constructor, we call
  // destroy and then re-create the table
  dt.destroy()

  // Set the class and style here otherwise the width
  // might become a fixed width
  table.setAttribute('class', other_args.classes)
  table.setAttribute('style', other_args.style)

  dt = new ITable(table, dt_args)
  if (other_args.caption) {
    dt.dt.caption(other_args.caption)
  }

  dt.selected_rows = other_args.selected_rows;

  function export_selected_rows() {
    Streamlit.setComponentValue({ selected_rows: dt.selected_rows });
  };

  dt.dt.on('select', function (e: any, dt: any, type: any, indexes: any) {
    export_selected_rows();
  });

  dt.dt.on('deselect', function (e: any, dt: any, type: any, indexes: any) {
    export_selected_rows();
  });

  // we recalculate the height
  Streamlit.setFrameHeight()
}

// connect the render function to Streamlit
Streamlit.events.addEventListener(Streamlit.RENDER_EVENT, onRender)
Streamlit.setComponentReady()
