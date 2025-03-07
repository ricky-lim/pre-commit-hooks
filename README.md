# Pre-commit Hooks

## Available Hooks

### check-changelog

Ensures that your project maintains a properly formatted `CHANGELOG.md` file with a NEXT section for upcoming changes.

Features:
- Validates that CHANGELOG.md exists
- Ensures it contains exactly one ## NEXT section followed by an empty line
- Can run at commit or push time
- Configurable to run only on specific branch types (feature, bugfix, etc.)
- Can verify CHANGELOG.md is included in the commit

## Installation

Add the following to your `.pre-commit-config.yaml`

```yaml
repos:
-   repo: https://github.com/ricky-lim/pre-commit-hooks
    rev: v0.1.0  # Use the specific version you want
    hooks:
    -   id: check-changelog
```

For advanced configuration

```yaml
repos:
-   repo: https://github.com/ricky-lim/pre-commit-hooks
    rev: v0.1.0
    hooks:
    -   id: check-changelog
        args:
          # Custom changelog filename
          - --filename=CHANGES.md
          # Only run on these branch types
          - --branch-prefixes=feature hotfix bugfix release
          # Run at push stage
          - --stage=pre-push
        # Only run at push time
        stages: [pre-push]
        # Always run, regardless of which files changed
        always_run: true
```
