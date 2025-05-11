import React, { useEffect, useState, useRef, useCallback } from "react";
import { ITable as ITableClass, set_or_remove_dark_class} from "dt_for_itables";
import { defaultProps, propTypes } from '../components/ITable.react.js';
import "dt_for_itables/dt_bundle.css";

const ITable = (props) => {
  const { id, caption, selected_rows, classes, style, dt_args, setProps } = props;

  const dtInstance = useRef(null);
  const emptyRowSelectionTimeout = useRef(null);
  const ignoreSelectEvents = useRef(false);

  const [state, setState] = useState({
    localDtArgs: dt_args,
    localCaption: caption,
    localSelectedRows: selected_rows
  });

  useEffect(() => {
    setState(prevState => ({
      ...prevState,
      localDtArgs: dt_args,
      localCaption: caption,
      localSelectedRows: selected_rows
    }));
  }, [dt_args, caption, selected_rows]);

  useEffect(() => {
    set_or_remove_dark_class();

    console.debug("Updating dt_args for DataTable(id='%s')", id);
    let dtArgs = { ...state.localDtArgs };

    function destroyDtInstance() {
      if (dtInstance.current) {
        if (emptyRowSelectionTimeout.current) {
          clearTimeout(emptyRowSelectionTimeout.current);
          emptyRowSelectionTimeout.current = null;
        }

        dtInstance.current.destroy();
        dtInstance.current = null;
      }
    }

    destroyDtInstance();

    dtInstance.current = new ITableClass("#".concat(id), dtArgs);
    dtInstance.current.dt.on('select', export_selected_rows);
    dtInstance.current.dt.on('deselect', export_selected_rows);


    return destroyDtInstance;
  }, [state.localDtArgs]);

  useEffect(() => {
    if (dtInstance.current) {
      console.debug("Updating caption for DataTable(id='%s'): %s", id, state.localCaption);
      dtInstance.current.dt.caption(state.localCaption);
    }
  }, [state.localCaption]);

  useEffect(() => {
    if (dtInstance.current) {
      if (emptyRowSelectionTimeout.current) {
        clearTimeout(emptyRowSelectionTimeout.current);
        emptyRowSelectionTimeout.current = null;
      }

      const current_rows = dtInstance.current.selected_rows;
      if (current_rows.length == state.localSelectedRows.length) {
        if (current_rows.every((value, index) => value === state.localSelectedRows[index])) {
          return;
        }
      }

      console.info("Setting row selection for DataTable(id='%s') to ", id, state.localSelectedRows, "from ", current_rows);
      ignoreSelectEvents.current = true;
      dtInstance.current.selected_rows = state.localSelectedRows;
      ignoreSelectEvents.current = false;
    }
  }, [state.localSelectedRows]);

  const export_selected_rows = useCallback((e, dt, type, indexes) => {
    if (ignoreSelectEvents.current) return;

    const current_rows = dtInstance.current.selected_rows;

    function update_selected_rows(rows) {
      if (ignoreSelectEvents.current)
        return;

      console.debug("Selected rows have changed for DataTable(id='%s'): %s", id, rows);
      setProps({ selected_rows: rows });
    }

    if (emptyRowSelectionTimeout.current) {
      console.debug("Cancel empty rows for DataTable(id='%s'): %s", id, current_rows);
      clearTimeout(emptyRowSelectionTimeout.current);
      emptyRowSelectionTimeout.current = null;
    }

    if (current_rows.length === 0) {
      console.debug("Postponing empty row selection for DataTable(id='%s'): %s", id, current_rows);
      emptyRowSelectionTimeout.current = setTimeout(() => update_selected_rows(current_rows), 50);
    } else {
      update_selected_rows(current_rows);
    }
  }, []);

  return (
    <table id={id} className={classes} style={style}></table>
  );
}

ITable.defaultProps = defaultProps;
ITable.propTypes = propTypes;

export default ITable;
