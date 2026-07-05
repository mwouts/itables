import pathlib
from typing import Optional

import anywidget
import traitlets
from pyaggrid.javascript import get_pyaggrid_extension_arguments
from pyaggrid.typing import DataFrameOrSeries, PyAgGridOptions, Unpack
from pyaggrid.version import __version__


class AgGrid(anywidget.AnyWidget):
    """A Jupyter widget that renders a DataFrame with AG Grid"""

    _esm = pathlib.Path(__file__).parent / "static" / "widget.js"
    _css = pathlib.Path(__file__).parent / "static" / "widget.css"

    # public traits
    caption = traitlets.Unicode().tag(sync=True)
    classes = traitlets.Unicode().tag(sync=True)
    selected_rows = traitlets.List(traitlets.Int()).tag(sync=True)

    # this trait is private - use the 'style' property and setter
    _style = traitlets.Unicode().tag(sync=True)

    # private traits that relate to df or to the AG Grid arguments
    # (use .update() to update them)
    _grid_args = traitlets.Dict().tag(sync=True)

    def __init__(
        self,
        df: Optional[DataFrameOrSeries] = None,
        caption: Optional[str] = None,
        **kwargs: Unpack[PyAgGridOptions],
    ) -> None:
        super().__init__()
        grid_args, other_args = get_pyaggrid_extension_arguments(df, caption, **kwargs)
        self._df = df
        self.caption = other_args.pop("caption") or ""
        self.classes = other_args.pop("classes")
        self._style = other_args.pop("style")
        self.selected_rows = other_args.pop("selected_rows")

        self._grid_args = grid_args
        assert not other_args, other_args

    def update(
        self,
        df: Optional[DataFrameOrSeries] = None,
        caption: Optional[str] = None,
        **kwargs: Unpack[PyAgGridOptions],
    ) -> None:
        """
        Update either the table data, attributes, or the arguments
        passed to AG Grid.
        """
        if df is None:
            df = self._df
        if "selected_rows" not in kwargs:
            kwargs["selected_rows"] = self.selected_rows or []
        if caption is None and self.caption is not None:
            caption = self.caption
        if "classes" not in kwargs:
            kwargs["classes"] = self.classes
        if "style" not in kwargs:
            kwargs["style"] = self.style

        grid_args, other_args = get_pyaggrid_extension_arguments(df, caption, **kwargs)

        self.classes = other_args.pop("classes")
        self._style = other_args.pop("style")
        self.caption = other_args.pop("caption") or ""

        if df is None:
            # keep the current data
            grid_args["data_json"] = self._grid_args.get("data_json", "[]")
            if "downsampling_warning" in self._grid_args:
                grid_args["downsampling_warning"] = self._grid_args[
                    "downsampling_warning"
                ]
            if not grid_args["grid_options"].get("columnDefs"):
                grid_args["grid_options"]["columnDefs"] = self._grid_args[
                    "grid_options"
                ].get("columnDefs", [])
        else:
            self._df = df

        if grid_args != self._grid_args:
            self._grid_args = grid_args

        self.selected_rows = other_args.pop("selected_rows")

    @property
    def df(self) -> Optional[DataFrameOrSeries]:
        return self._df

    @df.setter
    def df(self, df: Optional[DataFrameOrSeries]) -> None:
        self.update(df)

    @property
    def style(self) -> str:
        return self._style

    @style.setter
    def style(self, style: str):
        self._style = style


__all__ = ["AgGrid", "__version__"]
