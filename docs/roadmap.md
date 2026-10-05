# Project Roadmap

The mission of NaSuno is to provide the standard, high-fidelity, open-source audio forensics and watermark neutralization framework for AI-generated music.

---

## Phase 1: Core Modernization & Architectural Hardening (Completed - v2.0.0)

- [x] Complete restructuring into enterprise modular architecture (`src/nasuno`).
- [x] Contract-based interfaces (`BaseDetector`, `BaseRemover`, protocols).
- [x] Unified CLI engine (`nasuno` command with subcommands).
- [x] Strict isolation of signal processing from I/O and orchestration.
- [x] Environment variable configuration system with typed profiles.
- [x] Docker multi-stage containerization.
- [x] Comprehensive CI/CD multi-OS test matrix.
- [x] Professional open-source governance suite (Zero Emojis, Code of Conduct, Contributing, Security).

---

## Phase 2: Definitive DAG Pipeline, Perceptual Masking & Neural Neutralization (Completed - v3.0.0)

- [x] DAG Pipeline Orchestration with Kahn's topological sort and inter-stage budget recalculation.
- [x] Content Intelligence Engine with 8 multi-domain forensic analyzers.
- [x] Psychoacoustic Masking Engine (ISO 226 ATH, Schroeder spreading curves, power-law summation).
- [x] 25-Bark-Band ISO 226 Quality Firewall with content-adaptive gates and automatic stage rollback.
- [x] Minimum-Change Parameter Optimizer with discrete grid and binary search refinement.
- [x] 14 Specialized Forensic Removal Stages (Sprints 1-4: Mel, Neural Residual, Sync Disrupt, Upsampler, Classical, Resynthesis, Statistical, Quantization, Bandwidth, Environment, Bispectral, LPC Residual, Disclosure, Hash Disrupt).
- [x] Container Metadata Scrubber (targeted C2PA RIFF chunks, ID3 GEOB, BMFF UUID boxes).
- [x] Anti-forensic Sinc Resampling Round-Trip, Frame-Grid Sample Padding, and Content-Seeded Mastering Naturalizer.
- [x] 100% Pytest pass rate across all 52 core unit, integration, and CLI tests.

---

## Phase 3: Real-Time Streaming & High-Throughput Service (Q1 2027)

- [ ] Asynchronous streaming processor using WebSockets and low-latency ring buffers.
- [ ] FastAPI microservice layer with OpenAPI v3 specification.
- [ ] Kubernetes Helm chart and horizontal pod autoscaling configuration.
- [ ] Prometheus metrics exporter (processing latency, SNR preservation, throughput).

---

## Phase 4: Native Acceleration & Ecosystem (Q2 2027)

- [ ] Rust / C++ DSP extensions with AVX-512 and NEON SIMD optimizations.
- [ ] VST3 / AU audio plugin for direct digital audio workstation (DAW) integration.
- [ ] Browser-based WebAssembly (Wasm) client-side demonstration interface.
