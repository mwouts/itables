"""The itables.javascript module now lives in pydatatables.javascript"""

from pydatatables.javascript import *  # noqa: F401,F403
from pydatatables.javascript import (  # noqa: F401
    generate_init_offline_pydatatables_html,
    get_pydatatables_extension_arguments,
    set_pydatatables_repr_html_methods,
    to_html_datatable,
)

# The historical names of the itables functions
generate_init_offline_itables_html = generate_init_offline_pydatatables_html
get_itables_extension_arguments = get_pydatatables_extension_arguments
set_itables_repr_html_methods = set_pydatatables_repr_html_methods
