# Pre-commit Hooks

![Coverage](https://img.shields.io/badge/coverage-100.00%25-brightgreen)
![Test](https://github.com/ricky-lim/pre-commit-hooks/actions/workflows/test.yml/badge.svg)
[![Changelog](https://img.shields.io/badge/changelog-Common%20Changelog-blue.svg)](CHANGELOG.md)

## Available Hooks

### check-changelog

Ensures that your project maintains a properly formatted `CHANGELOG.md` file with a NEXT section for upcoming changes.

Features:
- Validates that CHANGELOG.md exists
- Ensures it contains exactly one ## NEXT section followed by an empty line
- Can run at pre-push or pre-commit stage
- Configurable to run only on specific branch types (feature, bugfix, etc.)

## Installation

Add the following to your `.pre-commit-config.yaml`

```yaml
repos:
-   repo: https://github.com/ricky-lim/pre-commit-hooks
    rev: v0.4.0  # Use the specific version you want
    hooks:
    -   id: check-changelog
```

For advanced configuration

```yaml
repos:
-   repo: https://github.com/ricky-lim/pre-commit-hooks
    rev: v0.4.0
    hooks:
    -   id: check-changelog
        args:
          # Custom changelog filename
          - --filename=CHANGES.md
          # Only run on these branch types
          - --branch-prefixes=feature hotfix bugfix release
        # Only run at push time
        stages: [pre-push]
        # Always run, regardless of which files changed
        always_run: true
```

## Develop

To set up your development environment, follow these steps:

1. **Clone the repository**:
    ```bash
    git clone https://github.com/ricky-lim/pre-commit-hooks.git
    cd pre-commit-hooks
    ```

2. **Create and activate a virtual environment**:
    ```bash
    uv venv --python=3.10
    source venv/bin/activate  #
    ```

3. **Install dependencies**:
    ```bash
    uv sync --dev
    uv pip install -e .
    ```

4.  **Run tests**:
    ```bash
    uv run pytest
    ```

5. **Install precommit**:
   ```bash
   pre-commit install
   ```

6. **Development workflow**:
    ```bash
    # Get latest updates
    git pull origin --tags

    # Run tests before committing
    pytest

    # Make changes and commit
    git add .
    git commit -m "Your descriptive commit message"
    ```
