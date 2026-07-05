import { AgGridTable } from "pyaggrid";

// The cleanup function is only called on unmount, not on data updates.
// We keep a registry so we can manually clean up the previous render when
// the component is updated in-place (same key, new data).
const cleanupRegistry = new Map();

const AgGridForStreamlit = (component) => {
  const { data, key, parentElement, setStateValue } = component;

  // Clean up the previous render for this key before creating a new one.
  cleanupRegistry.get(key)?.();
  cleanupRegistry.delete(key);

  const span = document.createElement("span");
  const container = span.appendChild(document.createElement("div"));
  parentElement.appendChild(span);

  const { grid_args, other_args } = data;

  container.setAttribute('class', other_args.classes);
  container.setAttribute('style', other_args.style);

  if (grid_args.downsampling_warning) {
    const warning = document.createElement('div');
    warning.className = 'pyaggrid-downsampling-warning';
    warning.innerHTML = grid_args.downsampling_warning;
    span.appendChild(warning);
  }
  if (other_args.caption) {
    const caption = document.createElement('div');
    caption.className = 'pyaggrid-caption';
    caption.style.textAlign = 'center';
    caption.textContent = other_args.caption;
    span.appendChild(caption);
  }

  const grid = new AgGridTable(container, grid_args);
  grid.selected_rows = other_args.selected_rows || [];

  function export_selected_rows() {
    setStateValue('selected_rows', grid.selected_rows);
  }

  // Sync state immediately so stale values from a previous render are cleared.
  export_selected_rows();
  grid.onSelectionChanged(export_selected_rows);

  const cleanup = () => {
    grid.destroy();
    span.remove();
    cleanupRegistry.delete(key);
  };
  cleanupRegistry.set(key, cleanup);
  return cleanup;
};

export default AgGridForStreamlit;
