import importlib.metadata
import pathlib
from typing import Sequence

import anywidget
import pandas as pd
import traitlets

from itables.javascript import (
    get_itables_extension_arguments,
    get_selected_rows_after_downsampling,
    get_selected_rows_before_downsampling,
)

try:
    __version__ = importlib.metadata.version("itables_anywidget")
except importlib.metadata.PackageNotFoundError:
    __version__ = "unknown"


class ITable(anywidget.AnyWidget):
    _esm = pathlib.Path(__file__).parent / "static" / "widget.js"
    _css = pathlib.Path(__file__).parent / "static" / "widget.css"

    data = traitlets.List(traitlets.List()).tag(sync=True)
    selected_rows = traitlets.List(traitlets.Int).tag(sync=True)

    caption = traitlets.Unicode().tag(sync=True)
    classes = traitlets.Unicode().tag(sync=True)
    style = traitlets.Unicode().tag(sync=True)
    downsampling_warning = traitlets.Unicode().tag(sync=True)
    dt_args = traitlets.Dict().tag(sync=True)

    def __init__(self, df=None, caption=None, selected_rows=None, **kwargs) -> None:
        super().__init__()

        if df is None:
            df = pd.DataFrame()
        self.df = df

        dt_args, other_args = get_itables_extension_arguments(
            df, caption, selected_rows, **kwargs
        )
        self.data = dt_args.pop("data")
        self.dt_args = dt_args
        self.classes = other_args.pop("classes")
        self.style = other_args.pop("style")
        self.caption = other_args.pop("caption") or ""
        self.downsampling_warning = other_args.pop("downsampling_warning") or ""
        self.selected_rows = other_args.pop("selected_rows")
        assert not other_args, other_args

    def update(self, df=None, caption=None, selected_rows=None, **kwargs):
        dt_args, other_args = get_itables_extension_arguments(
            df, caption, selected_rows, **kwargs
        )
        if df is not None:
            data = dt_args.pop("data")
            self.downsampling_warning = other_args.pop("downsampling_warning") or ""
            if self.data != data:
                self.data = data

        if self.dt_args != dt_args:
            self.dt_args = dt_args

        self.classes = other_args.pop("classes")
        self.style = other_args.pop("style")
        self.caption = other_args.pop("caption") or ""

        selected_rows = other_args.pop("selected_rows")
        if self.selected_rows != selected_rows:
            self.selected_rows = selected_rows

    def get_selected_rows(self) -> list[int]:
        return get_selected_rows_before_downsampling(
            self.selected_rows, len(self.df), len(self.data)
        )

    def set_selected_rows(self, selected_rows: Sequence[int]):
        selected_rows = get_selected_rows_after_downsampling(
            selected_rows, len(self.df), len(self.data)
        )
        if self.selected_rows != selected_rows:
            self.selected_rows = selected_rows
