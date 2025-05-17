import importlib.metadata
import pathlib

import anywidget
import traitlets
from typing_extensions import Unpack

from itables.javascript import get_itables_extension_arguments
from itables.typing import ITableOptions

try:
    __version__ = importlib.metadata.version("itables_anywidget")
except importlib.metadata.PackageNotFoundError:
    __version__ = "unknown"


class ITable(anywidget.AnyWidget):
    _esm = pathlib.Path(__file__).parent / "static" / "widget.js"
    _css = pathlib.Path(__file__).parent / "static" / "widget.css"

    # public traits
    caption = traitlets.Unicode().tag(sync=True)
    classes = traitlets.Unicode().tag(sync=True)
    style = traitlets.Unicode().tag(sync=True)
    selected_rows = traitlets.List(traitlets.Int()).tag(sync=True)

    # private traits that relate to df or to the DataTable arguments
    # (use .update() to update them)
    _dt_args = traitlets.Dict().tag(sync=True)

    def __init__(
        self,
        df=None,
        *args,
        **kwargs: Unpack[ITableOptions],
    ) -> None:
        super().__init__()
        dt_args, other_args = get_itables_extension_arguments(df, *args, **kwargs)
        self._df = df
        self.caption = other_args.pop("caption") or ""
        self.classes = other_args.pop("classes")
        self.style = other_args.pop("style")
        self.selected_rows = other_args.pop("selected_rows")

        self._dt_args = dt_args
        assert not other_args, other_args

    def update(
        self,
        df=None,
        *args,
        **kwargs: Unpack[ITableOptions],
    ):
        """
        Update either the table data, attributes, or the arguments passed
        to DataTable. Arguments that are not mentioned
        """
        dt_args_changed = False
        new_dt_args = self._dt_args.copy()
        for key, value in list(kwargs.items()):
            if value is None:
                dt_args_changed = True
                del kwargs[key]
                del new_dt_args[key]

        if df is None:
            df = self._df
        if "selected_rows" not in kwargs:
            kwargs["selected_rows"] = self.selected_rows
        if "caption" not in kwargs and self.caption is not None:
            kwargs["caption"] = self.caption
        if "classes" not in kwargs:
            kwargs["classes"] = self.classes
        if "style" not in kwargs:
            kwargs["style"] = self.style

        dt_args, other_args = get_itables_extension_arguments(df, *args, **kwargs)

        self.classes = other_args.pop("classes")
        self.style = other_args.pop("style")
        self.caption = other_args.pop("caption")

        if df is None:
            del dt_args["data_json"]
            del dt_args["filtered_row_count"]
            del dt_args["downsampling_warning"]
            dt_args.pop("table_html", None)
        else:
            self._df = df
            dt_args_changed = True

        for key, value in dt_args.items():
            if key not in new_dt_args or (new_dt_args[key] != value):
                new_dt_args[key] = value
                dt_args_changed = True

        if dt_args_changed:
            self._dt_args = new_dt_args

        self.selected_rows = other_args.pop("selected_rows")

    @property
    def df(self):
        return self._df

    @df.setter
    def df(self, df):
        self.update(df)
