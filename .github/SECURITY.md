# Security Policy

## Supported Versions

We release patches and security updates for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 2.x     | Yes                |
| 1.x     | No (End of Life)   |
| < 1.0   | No                 |

---

## Reporting a Vulnerability

The NaSuno team takes security seriously. If you discover a vulnerability, please report it responsibly instead of opening a public GitHub issue.

### Reporting Procedure

1. Send an email to `security@nasuno.org` (or open a confidential GitHub Security Advisory).
2. Include the following details in your report:
   - Type of issue (e.g., buffer overflow, malicious audio payload processing, denial of service, memory leak)
   - Step-by-step instructions or proof-of-concept audio file to reproduce the issue
   - Affected versions and environments (operating system, Python version)
   - Proposed mitigation or fix, if available

### Response Timeline

* **Acknowledgment**: Within 48 hours of receipt.
* **Assessment & Confirmation**: Within 5 business days.
* **Fix & Advisory Release**: Coordinated with the reporter, typically within 14 to 30 days depending on severity.

---

## Security Architecture & Threat Model

Because NaSuno processes arbitrary binary audio formats from untrusted sources, binary media represents an attack surface for memory corruption, buffer overflows in codec libraries, and decompression Denial-of-Service (DoS) attacks. The following defensive safeguards are enforced across all runtime environments:

### 1. Audio Decompression Bombs & Resource Exhaustion
* **Threat**: Maliciously crafted audio files with headers specifying extreme sample rates (e.g. 192 kHz), 128 channels, or infinite durations causing Out-Of-Memory (OOM) crashes.
* **Mitigation**:
  1. Header inspection prior to full buffer decompression.
  2. Enforced maximum duration and sample rate thresholds in `AudioReader`.
  3. Chunked streaming processing (`StreamingProcessor`) that limits working memory to fixed ring buffers (< 256 MB) regardless of file length.

### 2. Numerical Instability & Undefined States
* **Threat**: Corrupted audio frames containing `NaN` (Not a Number), `Inf` (Infinity), or extreme floating-point amplitudes causing arithmetic exceptions or downstream DAC speaker damage.
* **Mitigation**:
  1. `cleanup_nans`: Every DSP input and output stage sanitizes arrays, substituting `NaN` and `Inf` with zeros.
  2. Hard clipping protection: `AudioWriter` clamps all output sample values strictly within `[-1.0, 1.0]`.

### 3. Unsafe Deserialization & Arbitrary Code Execution
* **Threat**: Python's `pickle` module or `eval()` can execute arbitrary machine code during model or configuration loading.
* **Mitigation**:
  1. NaSuno strictly forbids the use of `pickle` or `eval()`.
  2. All models, configuration profiles, and metadata use pure Python dataclasses and standard JSON serialization.

### 4. Container Sandboxing
* **Threat**: Remote code execution inside container environments compromising the host system.
* **Mitigation**:
  1. The official Dockerfile enforces an unprivileged runtime user (`nasuno`, UID 1000).
  2. Root filesystem write permissions are disabled outside `/data` and `/home/nasuno/.cache`.

