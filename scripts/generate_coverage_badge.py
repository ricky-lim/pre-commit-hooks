#!/usr/bin/env python3
"""Generate coverage badge from coverage.xml."""

import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Tuple


def generate_badge(coverage_xml_path: str) -> Tuple[float, str]:
    """Generate coverage badge from coverage.xml.

    Args:
        coverage_xml_path: Path to coverage.xml file

    Returns:
        Tuple containing coverage percentage and badge URL
    """
    tree = ET.parse(coverage_xml_path)
    root = tree.getroot()
    coverage = float(root.attrib["line-rate"]) * 100

    # Determine badge color
    if coverage >= 90:
        color = "brightgreen"
    elif coverage >= 80:
        color = "green"
    elif coverage >= 70:
        color = "yellowgreen"
    else:
        color = "red"

    badge_url = f"https://img.shields.io/badge/coverage-{coverage:.2f}%25-{color}"
    return coverage, badge_url


def main() -> int:
    """Main entry point."""
    coverage_xml = Path("coverage.xml")
    if not coverage_xml.exists():
        print("Error: coverage.xml not found")
        return 1

    try:
        coverage, badge_url = generate_badge(str(coverage_xml))
    except Exception as e:
        print(f"Error generating badge: {e}")
        return 1

    # Write badge markdown
    with open("coverage_badge.md", "w") as f:
        f.write(f"![Coverage]({badge_url})")

    return 0


if __name__ == "__main__":
    exit(main())
