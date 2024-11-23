import {
  Streamlit,
  StreamlitComponentBase,
  withStreamlitConnection,
} from "streamlit-component-lib"
import React, { ReactNode } from "react"
import DataTable from "dt_for_itables"

import "dt_for_itables/dt_bundle.css"

interface State {
  selected_rows: Array<number>
}

class ITable extends StreamlitComponentBase<State> {
  public state = { selected_rows: [] }
  public dt = new DataTable('#itable');

  public render = (): ReactNode => {
    const dt_args = this.props.args['dt_args'];
    const other_args = this.props.args['other_args'];

    if (other_args.downsampling_warning) {
      dt_args["fnInfoCallback"] = function (oSettings: any, iStart: number, iEnd: number, iMax: number, iTotal: number, sPre: string) {
        return sPre + ' (' +
          other_args.downsampling_warning + ')'
      }
    }

    dt_args['destroy'] = true;
    this.dt = new DataTable("#itable", dt_args);
    if (other_args.caption) {
      this.dt.caption(other_args.caption)
    }

    DataTable.set_selected_rows(this.dt, other_args.filtered_row_count, other_args.selected_rows);

    function export_selected_rows(e: any, dt: any, type: any, indexes: any) {
      Streamlit.setComponentValue({ selected_rows: DataTable.get_selected_rows(dt, other_args.filtered_row_count) });
    };

    this.dt.on('select', export_selected_rows);
    this.dt.on('deselect', export_selected_rows);

    return (
      <table id="itable" className={other_args.classes} style={other_args.style}></table>
    );
  }
}

export default withStreamlitConnection(ITable)
