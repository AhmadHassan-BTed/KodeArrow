# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Planned
- Streaming audio processing pipeline via WebSockets.
- Direct C++/Rust extensions for SIMD-accelerated FFT filterbanks.
- Web UI dashboard for interactive spectrogram visual inspections.

---

## [2.0.0] - 2026-09-29

### Added
- Enterprise-grade modular architecture adhering to strict Separation of Concerns (SoC) and Data Coupling.
- Contract-based interfaces (`AudioDetectorProtocol`, `AudioRemoverProtocol`, `BaseDetector`, `BaseRemover`).
- Unified CLI interface (`nasuno clean`, `nasuno detect`, `nasuno analyze`, `nasuno compare`, `nasuno benchmark`).
- Environment variable configuration engine with `.env.example` support.
- Multi-tier processing profiles: `gentle`, `moderate`, `aggressive`, and `extreme`.
- Multi-stage Docker containerization with non-root security context and multi-architecture support.
- GitHub Actions CI/CD matrix workflows (Python 3.9 through 3.13, CodeQL analysis, release automation).
- Open-source governance and health documentation suite.
- Comprehensive unit and integration test suites.

### Changed
- Refactored monolith scripts into isolated modules (`nasuno.core`, `nasuno.io`, `nasuno.dsp`, `nasuno.detectors`, `nasuno.removers`, `nasuno.optimization`, `nasuno.evaluation`).
- Replaced direct `print` statements with structured, configurable logging.
- Hardened all audio processing against NaN, Inf, and floating-point overflow conditions.

### Removed
- Removed 19 legacy root scripts and redundant files.
- Removed all emojis from codebase, comments, logs, and documentation to adhere to strict professional open-source standards.

---

## [1.0.0] - 2025-01-15

### Added
- Initial release of Suno AI audio watermark detection and spectral notch filtering script.
- Basic ID3 and RIFF chunk metadata stripper.
