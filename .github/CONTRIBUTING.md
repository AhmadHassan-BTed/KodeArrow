# Contributing to NaSuno

Thank you for your interest in contributing to NaSuno. We welcome contributions from developers, audio engineers, researchers, and open-source enthusiasts.

To maintain production standards, this repository enforces strict architecture guidelines:
* Separation of Concerns (SoC)
* High Functional Cohesion
* Data Coupling (no hidden shared state or circular dependencies)
* Contract-Based Programming (interfaces defined via `Protocol` and `ABC`)
* Zero Emojis policy across code, commits, and documentation

---

## Code of Conduct

All contributors must adhere to our [Code of Conduct](CODE_OF_CONDUCT.md). Please read it before participating.

---

## Getting Started

### Prerequisites

* Python 3.9+ (Python 3.11+ recommended)
* `git`
* Optional: `libsndfile1`, `ffmpeg` for advanced audio codecs

### Local Development Setup

1. Fork the repository on GitHub and clone your fork:
   ```bash
   git clone https://github.com/<your-username>/NaSuno.git
   cd NaSuno
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   # Windows PowerShell:
   .venv\Scripts\Activate.ps1
   # Linux/macOS:
   source .venv/bin/activate
   ```

3. Install dependencies in editable mode with development tooling:
   ```bash
   pip install --upgrade pip setuptools wheel
   pip install -e .
   pip install -r requirements-dev.txt
   ```

4. Verify your setup by running the test suite:
   ```bash
   pytest -v
   ```

---

## Architectural Guidelines

When adding or modifying components:

1. **Contracts First**: New detectors must inherit from `nasuno.detectors.base.BaseDetector` or conform to `AudioDetectorProtocol`. New removers must inherit from `nasuno.removers.base.BaseRemover` or conform to `AudioRemoverProtocol`.
2. **Data Coupling Only**: Functions and classes should exchange standard data types (`np.ndarray`, `AudioBuffer`, `DetectionResult`, `RemovalResult`, `ProcessingConfig`, `ProcessingStats`). Do not create god-objects or pass unbounded dictionaries.
3. **No Direct I/O in DSP Modules**: Signal processing modules (`nasuno.dsp`, `nasuno.detectors`, `nasuno.removers`) must only operate on memory buffers (`np.ndarray`, sample rates, parameters). Disk I/O belongs exclusively to `nasuno.io` and `nasuno.cli`.
4. **Graceful Degradation**: Optional dependencies (e.g., `librosa`, `soundfile`, `scikit-learn`, `torch`) must be imported conditionally with clear fallback or informative user warnings.

---

## Development Workflow

### Branching Model

* `main`: Protected production branch.
* Feature/Fix branches: Create branch from `main`:
  ```bash
  git checkout -b feature/adaptive-comb-filter
  git checkout -b fix/sample-rate-resampling
  ```

### Commit Message Conventions

We adhere to the [Conventional Commits](https://www.conventionalcommits.org/) standard:

* `feat: add adaptive harmonic notch filtering`
* `fix: correct nyquist frequency boundary check in STFT`
* `docs: update system design and pipeline documentation`
* `refactor: extract audio I/O adapters from legacy remover`
* `test: add unit tests for phase dispersion processor`
* `perf: optimize array slicing in chunked streamer`
* `chore: update github action python test matrix`

Do NOT include emojis in commit messages or code comments.

---

## Quality Assurance & Testing

### Running Tests

```bash
# Run complete test suite
pytest

# Run with verbose output and coverage
pytest -v --cov=nasuno --cov-report=term-missing
```

### Static Analysis and Formatting

We use standard tools for code quality:

```bash
# Format code
black src tests
isort src tests

# Static linting
flake8 src tests
ruff check src tests

# Type validation
mypy src
```

---

## Submitting a Pull Request

1. Push your branch to your GitHub fork:
   ```bash
   git push origin feature/your-feature-name
   ```
2. Open a Pull Request against the `main` branch.
3. Complete the Pull Request template checklist.
4. Ensure all CI checks pass (formatting, linting, tests).
5. Address code review feedback promptly.

---

## Security Vulnerabilities

Please do not report security vulnerabilities via public GitHub issues. Follow our [Security Policy](SECURITY.md) for responsible disclosure.
