from itables.show_config import show_config


def test_show_config_default(capsys, tmp_path):
    show_config(tmp_path)
    captured = capsys.readouterr()
    assert "No ITables config file found" in captured.out


def test_show_config_with_options(monkeypatch, capsys, tmp_path):
    (tmp_path / "itables.toml").write_text('maxBytes = "8K"')

    show_config(tmp_path)

    captured = capsys.readouterr()
    assert "ITables config file:" in captured.out
    assert "maxBytes: 8K" in captured.out
