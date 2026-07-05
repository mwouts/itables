import React from 'react';
import PropTypes from 'prop-types';
import { AgGrid as RealComponent } from '../LazyLoader';

/**
 * AgGrid is a dash component for AG Grid
 */
const AgGrid = (props) => {
    return (
        <React.Suspense fallback={null}>
            <RealComponent {...props} />
        </React.Suspense>
    );
};

AgGrid.defaultProps = {};

AgGrid.propTypes = {
    /**
     * The ID used to identify this component in Dash callbacks.
     */
    id: PropTypes.string.isRequired,

    /**
     * The table caption
     */
    caption: PropTypes.string,

    /**
     * The index of the selected rows (pass rowSelection to allow selection)
     */
    selected_rows: PropTypes.array.isRequired,

    /**
     * The style of the grid container
     */
    style: PropTypes.object.isRequired,

    /**
     * The classes of the grid container
     */
    classes: PropTypes.string.isRequired,

    /**
     * The arguments for AG Grid: the grid options, the data, and
     * the optional downsampling warning
     */
    grid_args: PropTypes.object.isRequired,

    /**
     * Dash-assigned callback that should be called to report property changes
     * to Dash, to make them available for callbacks.
     */
    setProps: PropTypes.func
};

export default AgGrid;
export const defaultProps = AgGrid.defaultProps;
export const propTypes = AgGrid.propTypes;
