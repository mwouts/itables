"""Activate the representation of Pandas dataframes as interactive tables"""
import pandas as pd
from .javascript import _datatables_repr_

pd.DataFrame._repr_html_ = _datatables_repr_
pd.Series._repr_html_ = _datatables_repr_
