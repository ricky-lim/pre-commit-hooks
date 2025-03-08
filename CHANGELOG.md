# Changelog
[![Common Changelog](https://common-changelog.org/badge.svg)](https://common-changelog.org)

## [0.4.1] - 2025-03-08

### Changed

- Renamed workflow file from `version_bump.yml` to `version_coverage_bump.yml` for clarity

## [0.4.0] - 2025-03-08

### Added

- Added unit tests with 100% coverage for `check_changelog.py`
  - Test branch prefix validation
  - Test changelog format checking
  - Test CLI argument handling
- Set up GitHub Actions workflow for continuous testing
  - Automated test execution on push and pull requests
  - Coverage reporting with badges
  - Badge showing current test status
- Enhanced project configuration
  - Added pytest-cov settings in `pyproject.toml`
  - Configured coverage report formats
  - Set minimum coverage threshold

## [0.3.2] - 2025-03-07

### Fixed

- Corrected the parser for branch prefixes in the CLI

## [0.3.1] - 2025-03-07

### Added

- Improved `README.md` to include setup instructions for the development environment

### Changed

- Updated to Python 3.10

## [0.3.0] - 2025-03-07

### Added

- Added unittest in the GitHub workflow

## [0.2.0] - 2025-03-07

### Added

- Added feature to check changelog
