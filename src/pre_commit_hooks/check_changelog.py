#!/usr/bin/env python3

import argparse
import re
import subprocess
import sys
from pathlib import Path
from typing import List, Optional, Sequence
import os

PASS = 0
FAIL = 1

def get_current_branch() -> str:
    """Get the current git branch name."""
    try:
        return subprocess.check_output(
            ["git", "symbolic-ref", "--short", "HEAD"], universal_newlines=True
        ).strip()
    except subprocess.CalledProcessError:
        return ""


def check_branch_prefix(branch: str, prefixes: List[str]) -> bool:
    """Check if the branch name has one of the specified prefixes."""
    for prefix in prefixes:
        if branch.startswith(prefix):
            return True
    return False


def check_changelog_exists(filename: str) -> bool:
    """Check if the CHANGELOG.md file exists."""
    return Path(filename).is_file()


def check_next_section(filename: str) -> bool:
    """Check if the CHANGELOG.md file contains '## NEXT' followed by an empty line."""
    try:
        with open(filename, "r") as f:
            content = f.read()

            # Look for '## NEXT' followed by a newline and another newline
            pattern = r"## NEXT\n\n"
            matches = re.findall(pattern, content)
            
            # Check for exactly one match
            if len(matches) == 1:
                return True

            return False
    except Exception as e:
        print(f"Error reading {filename}: {e}")
        return False


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--filename", default="CHANGELOG.md", help="Name of the changelog file to check"
    )
    parser.add_argument(
        "--branch-prefixes",
        nargs="+",
        default=["feature", "hotfix", "bugfix", "other", "release"],
        help="Branch prefixes that should trigger the check",
    )
    parser.add_argument(
        "--all-branches",
        action="store_true",
        help="Run on all branches, ignoring branch prefixes",
    )
    parser.add_argument(
        "--stage",
        choices=["commit", "push"],
        default="commit",
        help="Stage at which to run the hook (commit or push)",
    )
    parser.add_argument(
        "filenames",
        nargs="*",
        help="Filenames to check (ignored, as we always check the changelog file)",
    )

    args = parser.parse_args(argv)

    # Check if we should run based on branch name
    current_branch = get_current_branch()
    if not args.all_branches and not check_branch_prefix(
        current_branch, args.branch_prefixes
    ):
        print(f"Skipping changelog check on branch '{current_branch}'")
        return PASS
        
    # Only run on specified stage
    current_stage = os.environ.get("PRE_COMMIT_HOOK_STAGE", "commit")
    if args.stage != current_stage:
        print(f"Skipping changelog check at '{current_stage}' stage (configured for '{args.stage}' stage)")
        return PASS

    # Check if changelog file exists
    if not check_changelog_exists(args.filename):
        print(f"Error: {args.filename} does not exist")
        return FAIL

    # Check for ## NEXT section with empty line after it
    if not check_next_section(args.filename):
        print(
            f"Error: {args.filename} must contain exactly one '## NEXT' section.\n"
            f"The format must be:\n"
            f"## NEXT\n"
            f"<empty line>\n"
            f"No spaces after '## NEXT' are allowed, and there must be exactly one empty line after it."
        )
        return FAIL

    print(f"✓ {args.filename} is valid")
    return PASS


if __name__ == "__main__":
    sys.exit(main())
