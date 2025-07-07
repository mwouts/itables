from pathlib import Path
from typing import Union

from typing_extensions import Optional, Unpack

import itables.options as opt

from .javascript import (
    generate_init_offline_itables_html,
    replace_value,
    to_html_datatable,
)
from .typing import DataFrameOrSeries, ITableOptions
from .utils import read_package_file

_CONNECTED = True


def init_itables(
    connected: bool = False,
    dt_bundle: Optional[Union[Path, str]] = None,
) -> str:
    """Load the DataTables library and the corresponding css (if connected=False).

    Warning: make sure you keep the output of this cell when 'connected=False',
    otherwise the interactive tables will stop working.
    """
    if dt_bundle is None:
        dt_bundle = opt.dt_bundle
    global _CONNECTED
    _CONNECTED = connected

    html = read_package_file("html/init_datatables.html")

    if not connected:
        html = html + "\n" + generate_init_offline_itables_html(dt_bundle)

    return html


def DT(
    df: DataFrameOrSeries,
    caption: Optional[str] = None,
    **kwargs: Unpack[ITableOptions],
) -> str:
    """This is a version of 'to_html_datatable' that works in Shiny applications."""
    kwargs["connected"] = kwargs.get("connected", _CONNECTED)
    html = to_html_datatable(
        df,
        caption,
        **kwargs,
    )

    html = html.replace("<code>init_notebook_mode</code>", "<code>init_itables</code>")

    if "table_id" not in kwargs:
        return html

    script_end = "\n    });\n</script>\n"
    assert html.endswith(script_end)
    html = replace_value(
        html,
        "new ITable(table, dt_args);",
        "let dt = new ITable(table, dt_args);",
    )

    selected_rows_code = f"""
        function set_selected_rows_in_shiny(...args) {{
            Shiny.setInputValue('{kwargs["table_id"]}_selected_rows', dt.selected_rows);
        }};

        set_selected_rows_in_shiny();
        dt.on('select', set_selected_rows_in_shiny);
        dt.on('deselect', set_selected_rows_in_shiny);"""

    return html.removesuffix(script_end) + selected_rows_code + script_end
