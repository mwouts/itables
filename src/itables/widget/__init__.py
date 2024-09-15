import importlib.metadata
import pathlib

import anywidget
import traitlets

from itables.javascript import get_itables_extension_arguments

try:
    __version__ = importlib.metadata.version("itables_anywidget")
except importlib.metadata.PackageNotFoundError:
    __version__ = "unknown"


class ITable(anywidget.AnyWidget):
    _esm = pathlib.Path(__file__).parent / "static" / "widget.js"
    _css = pathlib.Path(__file__).parent / "static" / "widget.css"
    dt_args = traitlets.Dict().tag(sync=True)
    data = traitlets.List(traitlets.List()).tag(sync=True)
    selected_rows = traitlets.List(traitlets.Int).tag(sync=True)
    caption = traitlets.Unicode().tag(sync=True)
    classes = traitlets.Unicode().tag(sync=True)
    style = traitlets.Unicode().tag(sync=True)
    downsampling_warning = traitlets.Unicode().tag(sync=True)

    def __init__(self, df, **kwargs) -> None:
        super().__init__()
        itable_arguments = get_itables_extension_arguments(df, **kwargs)
        dt_args = itable_arguments["dt_args"]
        self.data = dt_args.pop("data")
        self.dt_args = dt_args
        other_args = itable_arguments["other_args"]
        self.classes = other_args.pop("classes")
        self.style = other_args.pop("style")
        self.caption = other_args.pop("caption") or ""
        self.downsampling_warning = other_args.pop("downsampling_warning") or ""
        assert not other_args, other_args
