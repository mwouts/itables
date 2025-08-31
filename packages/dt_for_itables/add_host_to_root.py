#! /usr/bin/env python3
"""This is a Python script that modifies the dt_bundle.css to
add :host to each :root selector. This ensures that the styles
works in Marimo which uses Shadow DOM.
"""

import argparse
import re
import sys
import warnings


def add_host_to_root(css_content: str) -> str:
    """
    Add :host to each :root selector in the given CSS content.
    """
    if ":host" in css_content:
        raise ValueError("The CSS content already contains ':host'")

    # If the content is empty, return it as is
    if not css_content.strip():
        return css_content

    # Process each rule separately
    def process_rule(match):
        spaces_before = match.group(1)
        selector_group = match.group(2)
        properties = match.group(3)

        # Extract trailing whitespace from selector_group
        stripped_selector_group = selector_group.rstrip()
        spaces_after = selector_group[len(stripped_selector_group) :]
        selector_group = stripped_selector_group

        # If no :root in the selector, return the rule as is
        if ":root" not in selector_group:
            return f"{spaces_before}{selector_group}{spaces_after}{properties}"

        new_selectors = []

        # Split by commas to get individual selectors
        for selector in selector_group.split(","):
            striped_selector = selector.lstrip()
            new_selectors.append(striped_selector)
            if not striped_selector.startswith(":root"):
                continue
            if striped_selector == ":root" or striped_selector.startswith(
                (":root ", ":root.", ":root[")
            ):
                new_selectors.append(striped_selector.replace(":root", ":host", 1))
            else:
                warnings.warn(
                    f"Selector '{striped_selector}' contains ':root' but is not a simple ':root' selector. "
                    "It will not be modified."
                )

        return f"{spaces_before}{(', ').join(new_selectors)}{spaces_after}{properties}"

    # Match CSS rules: selector(s) { properties }
    pattern = r"(\s*)([^{]+)({[^}]*})"
    return re.sub(pattern, process_rule, css_content)


def main(argv):
    parser = argparse.ArgumentParser(
        description="Add :host to each :root selector in a CSS file."
    )
    parser.add_argument("css_file", help="Path to the CSS file to modify")
    args = parser.parse_args(argv[1:])

    with open(args.css_file, "r") as file:
        css_content = file.read()

    modified_content = add_host_to_root(css_content)

    with open(args.css_file, "w") as file:
        file.write(modified_content)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
