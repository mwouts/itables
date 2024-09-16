import importlib.metadata
import pathlib

import anywidget
import pandas as pd
import traitlets

from itables.javascript import get_itables_extension_arguments

try:
    __version__ = importlib.metadata.version("itables_anywidget")
except importlib.metadata.PackageNotFoundError:
    __version__ = "unknown"


class ITable(anywidget.AnyWidget):
    _esm = pathlib.Path(__file__).parent / "static" / "widget.js"
    _css = pathlib.Path(__file__).parent / "static" / "widget.css"

    full_row_count = traitlets.Int().tag(sync=True)
    data = traitlets.List(traitlets.List()).tag(sync=True)
    selected_rows = traitlets.List(traitlets.Int).tag(sync=True)
    destroy_and_recreate = traitlets.Int(0).tag(sync=True)

    caption = traitlets.Unicode().tag(sync=True)
    classes = traitlets.Unicode().tag(sync=True)
    style = traitlets.Unicode().tag(sync=True)
    downsampling_warning = traitlets.Unicode().tag(sync=True)
    dt_args = traitlets.Dict().tag(sync=True)

    def __init__(self, df=None, caption=None, selected_rows=None, **kwargs) -> None:
        super().__init__()

        if df is None:
            df = pd.DataFrame()

        dt_args, other_args = get_itables_extension_arguments(
            df, caption, selected_rows, **kwargs
        )
        self.full_row_count = other_args.pop("full_row_count")
        self.data = dt_args.pop("data")
        self.dt_args = dt_args
        self.classes = other_args.pop("classes")
        self.style = other_args.pop("style")
        self.caption = other_args.pop("caption") or ""
        self.downsampling_warning = other_args.pop("downsampling_warning") or ""
        self.selected_rows = other_args.pop("selected_rows") or []
        assert not other_args, other_args

    def update(self, df=None, caption=None, selected_rows=None, **kwargs):
        dt_args, other_args = get_itables_extension_arguments(
            df, caption, selected_rows, **kwargs
        )

        if df is not None:
            data = dt_args.pop("data")
            self.downsampling_warning = other_args.pop("downsampling_warning") or ""
            if self.dt_args != dt_args:
                self.dt_args = dt_args
            if self.data != data:
                self.data = data
        else:
            data = dt_args.pop("data")
            if "columns" not in dt_args:
                dt_args["columns"] = self.dt_args["columns"]
            if self.dt_args != dt_args:
                self.dt_args = dt_args

        self.classes = other_args.pop("classes")
        self.style = other_args.pop("style")
        self.caption = other_args.pop("caption") or ""

        selected_rows = other_args.pop("selected_rows")
        if selected_rows is not None and self.selected_rows != selected_rows:
            self.selected_rows = selected_rows

        self.destroy_and_recreate += 1
