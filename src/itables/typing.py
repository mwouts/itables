from typing import Literal, TypeAlias

import numpy as np
import pandas as pd

DataFrame: TypeAlias = pd.DataFrame
SeriesOrDataFrame: TypeAlias = pd.DataFrame | pd.Series | np.ndarray

try:
    import pandas.io.formats.style as pd_style
except ImportError:
    pd_style = None
else:
    SeriesOrDataFrame = SeriesOrDataFrame | pd_style.Styler

try:
    import polars as pl
except ImportError:
    pl = None
else:
    DataFrame = DataFrame | pl.DataFrame
    SeriesOrDataFrame = SeriesOrDataFrame | pl.DataFrame | pl.Series

ColumnFiltersType: TypeAlias = Literal["header", "footer", False]
