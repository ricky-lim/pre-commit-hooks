import pytest
from pathlib import Path

VALID_CHANGELOG_CONTENT = "# Changelog\n\n## NEXT\n\nSome planned changes\n"
# Invalid NEXT section - missing empty line after it
INVALID_NEXT_SECTION = "# Changelog\n\n## NEXT\nSome planned changes\n"


@pytest.fixture
def script_path():
    """Get the path to the check_changelog script."""
    return Path("src", "pre_commit_hooks", "check_changelog.py")


@pytest.fixture
def valid_changelog(tmp_path):
    """Fixture that creates a valid changelog file."""
    changelog = tmp_path / "CHANGELOG.md"
    changelog.write_text(VALID_CHANGELOG_CONTENT)
    return changelog


@pytest.fixture
def invalid_changelog(tmp_path):
    """Fixture that creates a changelog file with an invalid NEXT section."""
    changelog = tmp_path / "CHANGELOG.md"
    changelog.write_text(INVALID_NEXT_SECTION)
    return changelog
