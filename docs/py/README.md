This folders contains the `py:percent` representation of the documentation notebooks.

This is used to enforce formatting (black, isort) and quality checks (ruff, pyright) on the documentation.

NB: These files are kept in sync with the markdown documentation thanks to our Jupytext pre-commit hook in `.pre-commit-config.yaml`. You can edit either the `.py` or `.md` version and the pre-commit hook will update the other.
