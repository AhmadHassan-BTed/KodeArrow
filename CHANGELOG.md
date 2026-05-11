# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.5.0] - 2026-05-11
### Added
- Professional modular architecture under the `kode_arrow/` package.
- Dual-version support (Standard and R-Edition).
- Environment variable management using `.env`.
- Professional documentation (`CONTRIBUTING.md`, `SECURITY.md`, `ROADMAP.md`).
- Centralized logging and configuration validation.
- Abstract `BaseApp` class for enforced modularity.

### Changed
- Relocated historical versions to the `archive/` directory.
- Refactored `FirebaseService` to be independent of UI logic.
- Standardized all internal imports and pathing.

### Fixed
- Hardcoded Firebase credentials removed from source code.
- Path resolution issues for icons and assets.

## [2.0.0] - 2024-01-15
### Added
- Firestore integration for premium device management.
- Installer scripts for MSI deployment.
- Research data collection (ControlGroup).

## [1.0.0] - 2023-06-20
### Added
- Initial release with basic Alt-key hotkeys.
- System tray integration.
