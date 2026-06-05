import React from 'react';
import PropTypes from 'prop-types';
import { PyDataTablesRenderer as RealComponent } from '../LazyLoader';

/**
 * PyDataTablesRenderer is a dash component for PyDataTablesRenderers
 */
const PyDataTablesRenderer = (props) => {
    return (
        <React.Suspense fallback={null}>
            <RealComponent {...props} />
        </React.Suspense>
    );
};

PyDataTablesRenderer.defaultProps = {};

PyDataTablesRenderer.propTypes = {
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

export default PyDataTablesRenderer;
export const defaultProps = PyDataTablesRenderer.defaultProps;
export const propTypes = PyDataTablesRenderer.propTypes;
