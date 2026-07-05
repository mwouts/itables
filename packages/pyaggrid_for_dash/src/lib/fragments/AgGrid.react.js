import React, { useEffect, useRef } from "react";
import { AgGridTable } from "pyaggrid";
import { defaultProps, propTypes } from '../components/AgGrid.react.js';

const AgGrid = (props) => {
  const { id, caption, selected_rows, classes, style, grid_args, setProps } = props;

  const gridInstance = useRef(null);
  const containerRef = useRef(null);
  const ignoreSelectEvents = useRef(false);
  const selectedRowsRef = useRef(selected_rows);
  selectedRowsRef.current = selected_rows;

  useEffect(() => {
    console.debug("Updating grid_args for AgGrid(id='%s')", id);

    function destroyGridInstance() {
      if (gridInstance.current) {
        gridInstance.current.destroy();
        gridInstance.current = null;
      }
    }

    destroyGridInstance();

    gridInstance.current = new AgGridTable(containerRef.current, grid_args);
    gridInstance.current.onSelectionChanged(() => {
      if (ignoreSelectEvents.current) return;
      if (setProps) {
        setProps({ selected_rows: gridInstance.current.selected_rows });
      }
    });

    ignoreSelectEvents.current = true;
    gridInstance.current.selected_rows = selectedRowsRef.current || [];
    ignoreSelectEvents.current = false;

    return destroyGridInstance;
  }, [grid_args]);

  useEffect(() => {
    if (!gridInstance.current) return;

    const current_rows = gridInstance.current.selected_rows;
    const target = selected_rows || [];
    if (current_rows.length === target.length) {
      if (current_rows.every((value, index) => value === target[index])) {
        return;
      }
    }

    console.info("Setting row selection for AgGrid(id='%s') to ", id, target, "from ", current_rows);
    ignoreSelectEvents.current = true;
    gridInstance.current.selected_rows = target;
    ignoreSelectEvents.current = false;
  }, [selected_rows]);

  return (
    <div id={id} className="pyaggrid-dash">
      <div ref={containerRef} className={classes} style={style}></div>
      {grid_args.downsampling_warning ? (
        <div
          className="pyaggrid-downsampling-warning"
          dangerouslySetInnerHTML={{ __html: grid_args.downsampling_warning }}
        ></div>
      ) : null}
      {caption ? (
        <div className="pyaggrid-caption" style={{ textAlign: 'center' }}>{caption}</div>
      ) : null}
    </div>
  );
};

AgGrid.defaultProps = defaultProps;
AgGrid.propTypes = propTypes;

export default AgGrid;
