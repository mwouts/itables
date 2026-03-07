import type { FrontendRenderer, FrontendState } from "@streamlit/component-v2-lib"

import { ITable, set_or_remove_dark_class } from "dt_for_itables"

interface ITableState extends FrontendState {
  selected_rows: number[];
}

interface ITableData {
  dt_args: object;
  other_args: {
    classes: string;
    style: string;
    caption?: string;
    selected_rows: number[];
  };
}

const ITableForStreamlit: FrontendRenderer<ITableState, ITableData> = (component) => {
  const { data, parentElement, setStateValue } = component;

  set_or_remove_dark_class();

  // Create a table element
  const span = document.createElement("span");
  const table = span.appendChild(document.createElement("table"));
  parentElement.appendChild(span);

  const { dt_args, other_args } = data;

  // Set the class and style here otherwise the width
  // might become a fixed width
  table.setAttribute('class', other_args.classes);
  table.setAttribute('style', other_args.style);

  let dt = new ITable(table, dt_args);
  if (other_args.caption) {
    dt.dt.caption(other_args.caption);
  }

  dt.selected_rows = other_args.selected_rows;

  function export_selected_rows() {
    setStateValue('selected_rows', dt.selected_rows);
  }

  dt.dt.on('select', function (e: any, dt: any, type: any, indexes: any) {
    export_selected_rows();
  });

  dt.dt.on('deselect', function (e: any, dt: any, type: any, indexes: any) {
    export_selected_rows();
  });

  return () => {
    dt.destroy();
    span.remove();
  };
};

export default ITableForStreamlit;
