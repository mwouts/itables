import pytest

from itables.config import get_config_file, load_config_file


def test_get_config_current_directory(tmp_path):
    (tmp_path / "itables.toml").write_text('classes = ["compact", "display", "nowrap"]')

    config_file = get_config_file(tmp_path)
    assert config_file is not None
    config = load_config_file(config_file)
    assert config == {"classes": ["compact", "display", "nowrap"]}


def test_get_config_parent_directory(tmp_path):
    (tmp_path / "itables.toml").write_text('classes = ["compact", "display", "nowrap"]')
    tmp_path_child = tmp_path / "child"
    tmp_path_child.mkdir()

    config_file = get_config_file(tmp_path_child)
    assert config_file is not None
    config = load_config_file(config_file)
    assert config == {"classes": ["compact", "display", "nowrap"]}


def test_get_config_file_from_pyproject(tmp_path):
    (tmp_path / "pyproject.toml").write_text(
        '[tool.itables]\nclasses = ["compact", "display", "nowrap"]'
    )

    config_file = get_config_file(tmp_path)
    assert config_file is not None
    config = load_config_file(config_file)
    assert config == {"classes": ["compact", "display", "nowrap"]}


def test_helpful_message_when_config_is_incorrect(tmp_path):
    (tmp_path / "itables.toml").write_text("classes = ")

    config_file = get_config_file(tmp_path)
    assert config_file is not None
    with pytest.raises(
        ValueError,
        match=f"Failed to load ITables config from {tmp_path / 'itables.toml'}",
    ):
        load_config_file(config_file)
