# ITables Development Guide for AI Agents

## Project Overview

ITables transforms Pandas and Polars DataFrames into interactive [DataTables](https://datatables.net/) in Jupyter notebooks and Python applications. It's a display-only library with **optional dependencies**: pandas/numpy for Pandas support, polars/pyarrow for Polars support - neither is required.

**Core Architecture:**
- `src/itables/javascript.py`: Main module with `show()`, `init_notebook_mode()`, `to_html_datatable()` functions
- `src/itables/datatables_format.py`: DataFrame → DataTables JSON conversion, handles Pandas and Polars separately
- `src/itables/options.py`: Global default options (documented at mwouts.github.io/itables/options/)
- `src/itables/config.py`: TOML config file loading from `itables.toml` or `pyproject.toml` [tool.itables]
- `src/itables/downsample.py`: Limits table size via maxBytes/maxRows/maxColumns before rendering
- `packages/*`: 4 npm packages building JavaScript bundles (dt_for_itables, anywidget, dash, streamlit)

**Multi-Platform Support:**
- **Notebooks**: Jupyter Lab/Notebook, VS Code, Google Colab, Kaggle (HTML injection via IPython.display)
- **Applications**: Dash (`src/itables/dash.py` → `itables_for_dash`), Streamlit (`streamlit.py`), Shiny (`shiny.py`), Jupyter Widget (`widget/`)

## Development Workflow

### Environment Setup
```bash
mamba env create --file environment.yml  # or conda
conda activate itables
pre-commit install
pip install -e .
```

### Testing Commands
```bash
pytest                    # Run all tests
pytest -n 4              # Parallel execution with 4 workers
pytest tests/test_foo.py # Specific test file
pytest --cov=./ --cov-report=xml  # With coverage (CI uses this)
```

### Build Process
JavaScript must be built before Python package installation:
```bash
cd packages && npm run build  # Builds all 4 npm packages
# Outputs to src/itables/html/, src/itables_for_dash/, src/itables/widget/static/, etc.
```

The build is automatic via `hatch-jupyter-builder` in `pyproject.toml` when doing `pip install -e .` - you rarely need to run npm manually unless modifying JS.

### Documentation
```bash
python -m ipykernel install --name itables --user  # One-time kernel setup
jupyter book build docs
# Open docs/_build/html/index.html
```
Documentation uses Jupytext: `.md` files in `docs/` sync with `.py` files in `docs/py/`.

## Code Patterns & Conventions

### Optional Imports Pattern
Pandas/Polars imports **must be inside functions** to keep them optional:
```python
def _format_pandas_series(x):
    import pandas as pd  # ✓ Correct - lazy import
    import pandas.io.formats.format as fmt
    # ... use pandas ...

# import pandas as pd  # ✗ Wrong - makes pandas required
```

### Type Checking
- Uses TypedDict (`ITableOptions`, `DTForITablesOptions`) for configuration validation
- `check_itable_arguments()` validates options at runtime with typeguard>=4.4.1
- Pyright with strict mode on specific paths (see `pyproject.toml` [tool.pyright])
- Type stubs: pandas-stubs required in CI

### Testing Fixtures (tests/conftest.py)
- `df`: Parametrized fixture iterating all sample DataFrames
- `connected`: Tests both connected=True/False modes
- `use_to_html`: Tests pandas.to_html rendering path vs. direct conversion
- `lengthMenu`: Tests various pagination configurations
- Always include `monkeypatch` fixture to prevent environment variable pollution

### Configuration System
1. `ITABLES_CONFIG` env var → explicit path (empty string disables)
2. Current dir + parents: `itables.toml` or `pyproject.toml` [tool.itables]
3. User config dir: `~/.config/itables/itables.toml` (via platformdirs)
4. Stop at `ITABLES_CEILING_DIRECTORIES`

Options in `itables.options` are global defaults overridden by `show(**kwargs)` or `init_notebook_mode(**kwargs)`.

### JavaScript Integration
- `JavascriptFunction` strings start with `"function("` - converted via indirect eval
- `JavascriptCode` for arbitrary JS snippets (security: user must trust content)
- Keys in `keys_to_be_evaluated` list are evaled in JS (e.g., for DataTables callback options)

## Common Issues & Solutions

### "itables works with just polars" Branch Pattern
When supporting Polars without Pandas, check:
- All imports use lazy pattern (inside functions)
- Tests handle missing pandas with `pytest.skip("Pandas is not available")`
- `DataFrameOrSeries` type alias remains generic (`Any`) for both Pandas/Polars

### Downsampling Warning Display
Downsampling creates HTML links in warnings - set `allow_html=True` or use `<a>` escaping. Check `downsample()` return tuple: `(df, warning_html_string)`.

### Widget/App Mode Differences
Some options unavailable in apps (`_OPTIONS_NOT_AVAILABLE_IN_APP_MODE`):
- `connected`: Apps bundle JS; notebooks can use CDN
- `dt_url`, `display_logo_when_loading`: Notebook-specific

### Test Matrix (CI)
- Python 3.9-3.13, Pandas <2.0 / >=2.0 / pre-release / none
- typeguard <4 / <4.4.1 / latest (breaking changes in v4.4.1)
- Tests must pass without pandas+numpy OR polars+pyarrow installed

## File Organization

- `src/itables/`: Core library (pure Python)
- `src/itables_for_dash/`: Dash component (has ITable.py auto-generated)
- `packages/*/`: npm packages (esbuild bundles DataTables + extensions)
- `apps/`: Example apps (dash, marimo, shiny, streamlit, panel)
- `docs/`: Jupyter Book documentation (.md ↔ .py via Jupytext)
- `tests/`: pytest suite, uses fixtures from conftest.py

## Pre-commit Hooks
```bash
pre-commit run --all-files  # Manually run all hooks
```
Enforces: black, isort, ruff, jupytext (syncs docs/*.md ↔ docs/py/*.py)

## Release Checklist
See CI workflows in `.github/workflows/`:
- `continuous-integration.yml`: pre-commit, pyright, pytest matrix, codecov
- `publish.yml`: Build and publish to PyPI
- `publish-book.yml`: Deploy docs to GitHub Pages
