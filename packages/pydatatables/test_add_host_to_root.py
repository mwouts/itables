import pytest
from add_host_to_root import add_host_to_root, main


def test_add_host_to_root_example():
    """Test with the example given in the original file."""
    original_css = """
:root {}
:root.dark {}
html.dark, :root[data-bs-theme=dark] table.dataTable {}
"""
    expected_css = """
:root, :host {}
:root.dark, :host.dark {}
html.dark, :root[data-bs-theme=dark] table.dataTable, :host[data-bs-theme=dark] table.dataTable {}
"""
    assert add_host_to_root(original_css) == expected_css


def test_add_host_to_root_empty():
    """Test with empty CSS content."""
    assert add_host_to_root("") == ""


def test_add_host_to_root_no_root():
    """Test with CSS that doesn't contain :root selectors."""
    css = "body { color: red; }"
    assert add_host_to_root(css) == css


def test_add_host_to_root_with_host_raises_error():
    """Test that an error is raised if :host is already in the CSS."""
    css = ":host { color: red; }"
    with pytest.raises(ValueError):
        add_host_to_root(css)


def test_add_host_to_root_with_properties():
    """Test with CSS rules that have properties."""
    original_css = ":root { color: red; }"
    expected_css = ":root, :host { color: red; }"
    assert add_host_to_root(original_css) == expected_css


def test_add_host_to_root_with_multiple_rules():
    """Test with multiple CSS rules."""
    original_css = """
:root { color: red; }
:root.dark { color: blue; }
"""
    expected_css = """
:root, :host { color: red; }
:root.dark, :host.dark { color: blue; }
"""
    assert add_host_to_root(original_css) == expected_css


def test_add_host_to_root_complex_selectors():
    """Test with complex selectors containing :root."""
    original_css = """
html.dark, :root[data-bs-theme=dark] table.dataTable { color: white; }
:root[data-theme="light"] .element { background-color: white; }
"""
    expected_css = """
html.dark, :root[data-bs-theme=dark] table.dataTable, :host[data-bs-theme=dark] table.dataTable { color: white; }
:root[data-theme="light"] .element, :host[data-theme="light"] .element { background-color: white; }
"""
    assert add_host_to_root(original_css) == expected_css


def test_main_function(tmp_path):
    """Test the main function modifies the file as expected."""
    css_content = ":root { color: red; }"
    expected_content = ":root, :host { color: red; }"
    css_file = tmp_path / "test.css"
    css_file.write_text(css_content)

    main(["add_host_to_root.py", str(css_file)])
    result = css_file.read_text()
    assert result == expected_content
