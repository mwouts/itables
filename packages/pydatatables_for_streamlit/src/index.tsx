import type { FrontendRenderer, FrontendState } from "@streamlit/component-v2-lib"

import { PyDataTablesRenderer, set_or_remove_dark_class } from "pydatatables"

interface PyDataTablesRendererState extends FrontendState {
  selected_rows: number[];
}

interface PyDataTablesRendererData {
  dt_args: object;
  other_args: {
    classes: string;
    style: string;
    caption?: string;
    selected_rows: number[];
  };
}

// The cleanup function is only called on unmount, not on data updates.
// We keep a registry so we can manually clean up the previous render when
// the component is updated in-place (same key, new data).
const cleanupRegistry = new Map<string, () => void>();

const PyDataTablesRendererForStreamlit: FrontendRenderer<PyDataTablesRendererState, PyDataTablesRendererData> = (component) => {
  const { data, key, parentElement, setStateValue } = component;

  // Clean up the previous render for this key before creating a new one.
  cleanupRegistry.get(key)?.();
  cleanupRegistry.delete(key);

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

  let dt = new PyDataTablesRenderer(table, dt_args);
  if (other_args.caption) {
    dt.dt.caption(other_args.caption);
  }

  dt.selected_rows = other_args.selected_rows;

  function export_selected_rows() {
    setStateValue('selected_rows', dt.selected_rows);
  }

  // Sync state immediately so stale values from a previous render are cleared.
  export_selected_rows();

  dt.dt.on('select', function (e: any, dt: any, type: any, indexes: any) {
    export_selected_rows();
  });

  dt.dt.on('deselect', function (e: any, dt: any, type: any, indexes: any) {
    export_selected_rows();
  });

  const cleanup = () => {
    dt.destroy();
    span.remove();
    cleanupRegistry.delete(key);
  };
  cleanupRegistry.set(key, cleanup);
  return cleanup;
};

export default PyDataTablesRendererForStreamlit;
