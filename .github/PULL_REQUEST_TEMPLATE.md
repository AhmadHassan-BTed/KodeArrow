## Description

Provide a concise summary of the changes introduced in this pull request and the rationale behind them.

Closes #(issue)

---

## Type of Change

- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Architectural refactoring / code cleanup
- [ ] Documentation improvement
- [ ] CI/CD or build pipeline enhancement

---

## Architectural & Engineering Checklist

- [ ] Adheres to **Separation of Concerns** (DSP decoupled from I/O and orchestration)
- [ ] Enforces **Data Coupling** (standard typed data exchange, no shared global state)
- [ ] Follows **Contract-Based Programming** (`BaseDetector`, `BaseRemover`, or protocols implemented)
- [ ] No emojis added anywhere in code, comments, or documentation
- [ ] Graceful imports for any optional audio/ML dependencies (`try...except ImportError`)
- [ ] All new and existing tests pass locally (`pytest -v`)
- [ ] New unit or integration tests added for new behavior
- [ ] Documentation updated to reflect changes (README, `docs/`, docstrings)
- [ ] Conventional Commit message format used
