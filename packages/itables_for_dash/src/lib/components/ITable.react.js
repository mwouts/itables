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
     * Dash-assigned callback that should be called to report property changes
     * to Dash, to make them available for callbacks.
     */
    setProps: PropTypes.func
};

export default ITable;
export const defaultProps = ITable.defaultProps;
export const propTypes = ITable.propTypes;
