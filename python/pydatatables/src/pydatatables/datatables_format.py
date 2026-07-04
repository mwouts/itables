"""Table content serialization - these functions now live in itables_core.formatting"""

from itables_core.formatting import (  # noqa: F401
    _format_narwhals_series,
    _format_pandas_series,
    _format_polars_series,
    datatables_rows,
    escape_html_chars,
    escape_non_finite_float,
    generate_encoder,
)

__all__ = [
    "datatables_rows",
    "escape_html_chars",
    "escape_non_finite_float",
    "generate_encoder",
]
