import React from 'react';
import PropTypes from 'prop-types';
import { ITable as RealComponent } from '../LazyLoader';

/**
 * ITable is a dash component for ITables
 */
const ITable = (props) => {
    return (
        <React.Suspense fallback={null}>
            <RealComponent {...props} />
        </React.Suspense>
    );
};

ITable.defaultProps = {};

ITable.propTypes = {
    /**
     * The ID used to identify this component in Dash callbacks.
     */
    id: PropTypes.string.isRequired,

    /**
     * The table data - a list of lists with the same length as the columns.
     */
    data_json: PropTypes.string.isRequired,

    /**
     * The table columns - a list of dicts with a 'title' key.
     */
    columns: PropTypes.array.isRequired,

    /**
     * The table caption
     */
    caption: PropTypes.string,

    /**
     * The index of the selected rows (pass select=True to allow selection)
     */
    selected_rows: PropTypes.array.isRequired,

    /**
     * The table style
     */
    style: PropTypes.object.isRequired,

    /**
     * The table classes
     */
    classes: PropTypes.string.isRequired,

    /**
     * The arguments for DataTable e.g. select, buttons, layout etc.
     */
    dt_args: PropTypes.object.isRequired,

    /**
     * How many lines of the tables are not shown due to downsampling
     */
    filtered_row_count: PropTypes.number.isRequired,

    /**
     * The downsampling warning message, if any
     */
    downsampling_warning: PropTypes.string.isRequired,

    /**
     * Dash-assigned callback that should be called to report property changes
     * to Dash, to make them available for callbacks.
     */
    setProps: PropTypes.func
};

export default ITable;
export const defaultProps = ITable.defaultProps;
export const propTypes = ITable.propTypes;
