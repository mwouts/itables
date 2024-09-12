import importlib.metadata
import pathlib

import anywidget
import traitlets

from itables.javascript import get_itables_extension_arguments

try:
    __version__ = importlib.metadata.version("itables_anywidget")
except importlib.metadata.PackageNotFoundError:
    __version__ = "unknown"


class Itable(anywidget.AnyWidget):
    _esm = pathlib.Path(__file__).parent / "static" / "widget.js"
    _css = pathlib.Path(__file__).parent / "static" / "widget.css"
    dt_args = traitlets.Dict().tag(sync=True)
    other_args = traitlets.Dict().tag(sync=True)

    def __init__(self, df, **kwargs) -> None:
        super().__init__()
        itable_arguments = get_itables_extension_arguments(df, **kwargs)
        self.dt_args = itable_arguments["dt_args"]
        self.other_args = itable_arguments["other_args"]
