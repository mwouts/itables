import pytest
from pydatatables.config import tomllib, user_config_path
from pydatatables.show_config import show_config

if (tomllib is None) or (user_config_path is None):
    pytest.skip(
        reason="pydatatables[config] dependencies are not installed",
        allow_module_level=True,
    )


def test_show_config_default(capsys, tmp_path):
    show_config(tmp_path)
    captured = capsys.readouterr()
    assert "No PyDataTablesRenderers config file found" in captured.out


def test_show_config_with_options(monkeypatch, capsys, tmp_path):
    (tmp_path / "pydatatables.toml").write_text('maxBytes = "8K"')

    show_config(tmp_path)

    captured = capsys.readouterr()
    assert "PyDataTablesRenderers config file:" in captured.out
    assert "maxBytes: 8K" in captured.out
