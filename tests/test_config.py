import pytest

from itables.config import get_config_file, load_config_file


@pytest.fixture()
def no_itables_config(monkeypatch):
    monkeypatch.delenv("ITABLES_CONFIG", raising=False)
    yield
    monkeypatch.undo()


def test_get_config_current_directory(tmp_path, no_itables_config):
    (tmp_path / "itables.toml").write_text('classes = ["compact", "display", "nowrap"]')

    config_file = get_config_file(tmp_path)
    assert config_file is not None
    config = load_config_file(config_file)
    assert config == {"classes": ["compact", "display", "nowrap"]}


def test_get_config_parent_directory(tmp_path, no_itables_config):
    (tmp_path / "itables.toml").write_text('classes = ["compact", "display", "nowrap"]')
    tmp_path_child = tmp_path / "child"
    tmp_path_child.mkdir()

    config_file = get_config_file(tmp_path_child)
    assert config_file is not None
    config = load_config_file(config_file)
    assert config == {"classes": ["compact", "display", "nowrap"]}


def test_get_config_file_from_pyproject(tmp_path, no_itables_config):
    (tmp_path / "pyproject.toml").write_text(
        '[tool.itables]\nclasses = ["compact", "display", "nowrap"]'
    )

    config_file = get_config_file(tmp_path)
    assert config_file is not None
    config = load_config_file(config_file)
    assert config == {"classes": ["compact", "display", "nowrap"]}
