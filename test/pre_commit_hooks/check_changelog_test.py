from pathlib import Path
import tempfile
import pytest
import subprocess

from pre_commit_hooks.check_changelog import (
    get_current_branch,
    check_branch_prefix,
    check_next_section,
    main,
    PASS,
    FAIL,
)


def test_run_main(valid_changelog, script_path):
    result = subprocess.run(
        [
            "python",
            str(script_path),
            "--filename",
            str(valid_changelog),
            "--all-branches",
        ],
        capture_output=True,
        text=True,
    )
    assert "✓" in result.stdout
    assert result.returncode == PASS


def test_get_current_branch_error(monkeypatch):
    """Test get_current_branch when git command fails."""

    def mock_check_output(*args, **kwargs):
        raise subprocess.CalledProcessError(1, "git")

    monkeypatch.setattr("subprocess.check_output", mock_check_output)
    assert get_current_branch() == ""


@pytest.mark.parametrize(
    "branch_name, expected",
    [
        ("feature/my-feature", True),
        ("hotfix/my-hotfix", True),
        ("bugfix/my-bugfix", True),
        ("other/my-other", True),
        ("release/my-release", True),
        ("main", False),
        ("develop", False),
        ("master", False),
    ],
)
def test_branch_prefix_check(branch_name, expected):
    prefixes = ["feature", "hotfix", "bugfix", "other", "release"]
    assert check_branch_prefix(branch_name, prefixes) is expected


def test_empty_prefixes_list():
    assert check_branch_prefix("feature/my-feature", []) is False


@pytest.mark.parametrize(
    "content, expected",
    [
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
    ],
)
def test_next_section(content, expected):
    """Test check_next_section with various content patterns."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        changelog_path = Path(tmp_dir) / "CHANGELOG.md"
        changelog_path.write_text(content)

        assert check_next_section(str(changelog_path)) is expected


def test_check_next_section_file_error(tmp_path):
    """Test check_next_section with file read error."""
    non_readable = tmp_path / "non-readable.md"
    non_readable.write_text("")
    non_readable.chmod(0o000)  # Remove read permissions

    assert check_next_section(str(non_readable)) is False


def test_main_success(valid_changelog):
    """Test main function with a valid changelog file."""
    result = main(["--filename", str(valid_changelog), "--all-branches"])
    assert result == PASS


def test_main_missing_changelog(tmp_path):
    """Test main function with a missing changelog file."""
    changelog_path = tmp_path / "NONEXISTENT.md"

    result = main(["--filename", str(changelog_path), "--all-branches"])
    assert result == FAIL


def test_main_invalid_next_section(invalid_changelog):
    """Test main function with an invalid NEXT section."""

    result = main(["--filename", str(invalid_changelog), "--all-branches"])
    assert result == FAIL


def test_main_custom_branch_prefixes(valid_changelog, monkeypatch, capsys):
    """Test main function with custom branch prefixes."""

    mock_branch(monkeypatch, "custom/branch")

    # Test with non-matching prefix
    result = main(
        ["--filename", str(valid_changelog), "--branch-prefixes", "feature,other"]
    )
    captured = capsys.readouterr()
    assert "Skipping changelog check on branch 'custom/branch'" in captured.out
    assert result == PASS

    # Test with matching prefix
    result = main(
        ["--filename", str(valid_changelog), "--branch-prefixes", "custom,other"]
    )
    captured = capsys.readouterr()
    assert "✓" in captured.out
    assert result == PASS


def test_main_all_branches_flag(valid_changelog, monkeypatch, capsys):
    """Test main function with the --all-branches flag."""

    mock_branch(monkeypatch, "random/branch")

    result = main(["--filename", str(valid_changelog), "--all-branches"])
    captured = capsys.readouterr()
    assert "✓" in captured.out
    assert result == PASS


def test_main_custom_filename(tmp_path):
    """Test main function with a custom changelog filename."""
    changelog = tmp_path / "CUSTOM.md"
    changelog.write_text("# Changelog\n\n## NEXT\n\nSome planned changes\n")

    result = main(["--filename", str(changelog), "--all-branches"])
    assert result == PASS


def test_main_ignores_filenames_argument(valid_changelog):
    result = main(["--filename", str(valid_changelog), "somefile.txt"])
    assert result == PASS


def mock_branch(monkeypatch, branch_name):
    """Helper to mock git branch."""
    monkeypatch.setattr(
        "pre_commit_hooks.check_changelog.get_current_branch", lambda: branch_name
    )
