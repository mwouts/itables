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

  table.setAttribute('class', other_args.classes)
  table.setAttribute('style', other_args.style)

  var dt_args = (event as CustomEvent<RenderData>).detail.args.dt_args

  if(other_args.downsampling_warning) {
    dt_args["fnInfoCallback"] = function (oSettings:any, iStart:number, iEnd:number, iMax:number, iTotal:number, sPre:string) { return sPre + ' (' +
    other_args.downsampling_warning + ')' }
  }

  // As we can't pass the dt_args other than in the
  // DataTable constructor, we call
  // destroy and then re-create the table
  dt.destroy()
  dt = new DataTable(table, dt_args)
  if(other_args.caption) {
    dt.caption(other_args.caption)
  }

  // we recalculate the height
  Streamlit.setFrameHeight()
}

// connect the render function to Streamlit
Streamlit.events.addEventListener(Streamlit.RENDER_EVENT, onRender)
Streamlit.setComponentReady()
