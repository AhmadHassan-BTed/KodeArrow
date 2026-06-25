# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.5.1] - 2026-06-18
### Added
- **Production-grade process resilience module** (`kode_arrow/core/resilience.py`):
  - `NullStream` — prevents crashes when `sys.stdout`/`sys.stderr` are `None` in windowless `.exe` mode.
  - Global exception handlers (`sys.excepthook` + `threading.excepthook`) — catches all unhandled exceptions across all threads and logs them.
  - `WatchdogThread` — heartbeats every 30s, monitors keyboard hook health, auto-recovers dead hooks, and calls `SetThreadExecutionState` to prevent Windows from suspending the process.
  - `PowerEventListener` — listens for Windows sleep/wake events via hidden Win32 message window and triggers automatic hook re-registration on resume.
- Word and line selection hotkeys (`Ctrl + Alt + [u,i,o,j,k,l]`, with support for both Alts pressed simultaneously) mapping to `Ctrl + Shift + [Home/Up/End/Left/Down/Right]`.
- Word deletion and backspacing hotkeys (`Ctrl + Alt + [p, ;]`, with support for both Alts pressed simultaneously) mapping to `Ctrl + [Delete/Backspace]` for backspacing/deleting whole words.
- Refined repository directory structure by relocating the `research` folder to `docs/research` to clean up the root workspace.
- In-process retry loop (5 attempts) with full process restart as last resort.
- System tray retry loop (10 attempts) with full icon rebuild on each crash.
- Customizable base modifier key in shortcuts dashboard (Alt, Ctrl, Shift, Windows).
- Reset to Defaults button in shortcuts settings.
- Enter key binding for instant email submission in unlock dialog.
- Auto-generated `KodeArrow.txt` release notes placed next to the compiled executable on launch.
- Single-instance process enforcement on launch.

### Changed
- Replaced all `print()` calls with structured `logging` across the entire production codebase — eliminates silent `AttributeError` crashes in windowless mode.
- Upgraded logging to `RotatingFileHandler` (2MB max, 3 backups) — prevents unbounded log file growth.
- Smart `StreamHandler` that only attaches when real stdout exists (skips `NullStream` overhead).
- Thread-safe `reload_hotkeys()` with mutex lock.
- Telemetry network checks now run asynchronously off the keyboard hook thread to prevent OS-level hook timeouts.
- Log file now resolves to user home directory (`~/kodearrow.log`) to prevent permission errors when launched from system startup.

### Fixed
- **Critical: Application silently dying when running as windowless `.exe`** — caused by `print()` to `None` stdout, unrecoverable `pystray` crashes, and Windows invalidating keyboard hooks after sleep/hibernate.
- Keyboard hooks now automatically re-register after Windows sleep/hibernate/resume cycles.
- Process no longer classified as idle/suspendable by Windows power management.

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
