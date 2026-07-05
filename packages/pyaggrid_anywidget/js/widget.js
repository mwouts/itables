import { AgGridTable } from 'pyaggrid';

/* The attributes below are defined with traitlets in
   python/pyaggrid/src/pyaggrid/widget/__init__.py:
   _grid_args, caption, classes, _style, selected_rows */
function render({ model, el }) {
	el.classList.add('pyaggrid_anywidget');
	const container = document.createElement('div');
	const warning = document.createElement('div');
	warning.className = 'pyaggrid-downsampling-warning';
	const caption = document.createElement('div');
	caption.className = 'pyaggrid-caption';
	caption.style.textAlign = 'center';
	el.appendChild(container);
	el.appendChild(warning);
	el.appendChild(caption);

	function update_classes() {
		container.className = model.get('classes');
	}
	function update_style() {
		container.setAttribute('style', model.get('_style'));
	}
	function update_caption() {
		caption.textContent = model.get('caption') || '';
	}

	// Set initial values
	update_classes();
	update_style();
	update_caption();

	// Update the grid container when one of these change
	model.on('change:classes', update_classes);
	model.on('change:_style', update_style);
	model.on('change:caption', update_caption);

	let grid = null;

	let setting_selected_rows_from_model = false;
	function set_selected_rows_from_model() {
		// We use this variable to avoid triggering model updates!
		setting_selected_rows_from_model = true;
		grid.selected_rows = model.get('selected_rows');
		setting_selected_rows_from_model = false;
	}

	function export_selected_rows() {
		if (setting_selected_rows_from_model)
			return;

		model.set('selected_rows', grid.selected_rows);
		model.save_changes();
	}

	function update_grid() {
		if (grid) {
			grid.destroy();
		}

		const grid_args = model.get('_grid_args');
		warning.innerHTML = grid_args.downsampling_warning || '';
		grid = new AgGridTable(container, grid_args);
		grid.onSelectionChanged(export_selected_rows);
		set_selected_rows_from_model();
	}
	update_grid();

	model.on('change:_grid_args', update_grid);
	model.on('change:selected_rows', set_selected_rows_from_model);
}

export default { render };
