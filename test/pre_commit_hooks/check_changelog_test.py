from pathlib import Path
import tempfile
import pytest

from pre_commit_hooks.check_changelog import (
    check_branch_prefix,
    check_next_section,
)

@pytest.mark.parametrize("branch_name, expected", [
        ('feature/my-feature', True),
        ('hotfix/my-hotfix', True),
        ('bugfix/my-bugfix', True),
        ('other/my-other', True),
        ('release/my-release', True),
        ('main', False),
        ('develop', False),
        ('master', False),
])
def test_branch_prefix_check(branch_name, expected):
    prefixes = ['feature', 'hotfix', 'bugfix', 'other', 'release']
    assert check_branch_prefix(branch_name, prefixes) is expected


def test_empty_prefixes_list():
    assert check_branch_prefix("feature/my-feature", []) is False


@pytest.mark.parametrize("content, expected", [
    # Valid NEXT section with empty line after it
    ("# Changelog\n\n## NEXT\n\nSome planned changes\n", True),
    
    # NEXT section with no empty line after it
    ("# Changelog\n\n## NEXT\nSome planned changes\n", False),
    
    # No NEXT section
    ("# Changelog\n\n## v1.0.0\n\nSome changes\n", False),
    
    # NEXT section at beginning of file
    ("## NEXT\n\nSome planned changes\n", True),
    
    # NEXT section with spaces after it
    ("# Changelog\n\n## NEXT  \n\nSome planned changes\n", False),
    
    # Empty file
    ("", False),
    
    # Multiple NEXT sections - not allowed
    ("# Changelog\n\n## NEXT\n\nChanges\n\n## NEXT\n\nNo empty line", False),
])
def test_next_section(content, expected):
    """Test check_next_section with various content patterns."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        changelog_path = Path(tmp_dir) / "CHANGELOG.md"
        changelog_path.write_text(content)
        
        assert check_next_section(str(changelog_path)) is expected