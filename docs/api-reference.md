# NaSuno Python API Reference

This document provides a complete reference for the core Python classes, methods, and functions in the `nasuno` package.

---

## 1. Domain & Foundation Layer (`nasuno.core`)

### `AudioProcessingPipeline`
```python
from nasuno.core.pipeline import AudioProcessingPipeline
```
Decoupled audio orchestrator with dependency injection.

#### Constructor
```python
AudioProcessingPipeline(
    reader: Optional[AudioReader] = None,
    writer: Optional[AudioWriter] = None,
    scrubber: Optional[MetadataScrubber] = None,
    detectors: Optional[List[AudioDetectorProtocol]] = None,
    removers: Optional[List[AudioRemoverProtocol]] = None,
)
```

#### Methods
* `process_file(input_path: Union[str, Path], output_path: Union[str, Path], config: Optional[ProcessingConfig] = None) -> Tuple[str, ProcessingStats]`:
  Processes an input audio file through the registered detectors and removers, exports the cleaned audio, scrubs metadata, and returns the output path and telemetry stats.

---

### `AudioBuffer`
```python
from nasuno.core.models import AudioBuffer
```
Encapsulates an in-memory floating-point audio signal.

#### Attributes
* `data`: `np.ndarray` (shape: `(samples,)` for mono or `(channels, samples)` for multichannel, dtype: `float32` in `[-1.0, 1.0]`).
* `sample_rate`: `int` (sampling rate in Hz).
* `channels`: `int` (number of channels).
* `duration_seconds`: `float` (total duration in seconds).
* `num_samples`: `int` (number of frames).

#### Methods
* `to_mono() -> np.ndarray`: Returns a 1D mono downmix array.

---

### `ProcessingConfig`
```python
from nasuno.core.config import ProcessingConfig
```
Configuration parameters controlling DSP intensity and analysis parameters.

#### Factory Method
* `ProcessingConfig.get_profile(level: str) -> ProcessingConfig`:
  Returns a predefined configuration profile: `"gentle"`, `"moderate"`, `"aggressive"`, or `"extreme"`.

---

### `Settings`
```python
from nasuno.core.config import Settings
```
Application settings loaded from environment variables and `.env` files.

#### Factory Method
* `Settings.from_env() -> Settings`:
  Parses environment variables prefixed with `NASUNO_` and returns a typed `Settings` instance.

---

## 2. Audio I/O Layer (`nasuno.io`)

### `AudioReader`
```python
from nasuno.io.reader import AudioReader
```
Robust multi-engine audio reader with automatic fallback across `soundfile`, `scipy.io.wavfile`, and Python's standard `wave` module.

#### Methods
* `read(file_path: Union[str, Path]) -> AudioBuffer`:
  Loads an audio file into an `AudioBuffer`.

---

### `AudioWriter`
```python
from nasuno.io.writer import AudioWriter
```
Audio exporter with peak-limiting and bit-depth quantization.

#### Methods
* `write(buffer: AudioBuffer, file_path: Union[str, Path], subtype: str = "PCM_16", apply_dither: bool = True) -> Path`:
  Clamps samples, optionally applies TPDF dither, and writes to disk.

---

### `MetadataScrubber`
```python
from nasuno.io.metadata import MetadataScrubber
```
Removes container metadata without affecting audio samples.

#### Methods
* `scrub(file_path: Union[str, Path]) -> AudioMetadata`:
  Scrubs ID3 tags, RIFF chunks, and user comments from the target file in-place.

---

## 3. Digital Signal Processing Layer (`nasuno.dsp`)

```python
from nasuno.dsp.filters import apply_notch_filter, apply_comb_filter, apply_harmonic_filterbank
from nasuno.dsp.spectral import compute_stft, compute_istft, suppress_spectral_peaks
from nasuno.dsp.dynamics import apply_tpdf_dither, apply_phase_jitter
```

### Functions
* `apply_notch_filter(audio: np.ndarray, sr: int, freq: float, q: float = 30.0) -> np.ndarray`:
  Applies a digital notch filter at the specified frequency.
* `apply_comb_filter(audio: np.ndarray, sr: int, fundamental_freq: float, depth: float = 0.5) -> np.ndarray`:
  Suppresses periodic harmonic series with given fundamental frequency.
* `apply_harmonic_filterbank(audio: np.ndarray, sr: int, base_freq: float, num_harmonics: int = 5, q: float = 35.0) -> np.ndarray`:
  Filters a fundamental carrier frequency and its integer multiples.
* `compute_stft(audio: np.ndarray, n_fft: int = 2048, hop_length: Optional[int] = None) -> Tuple[np.ndarray, np.ndarray]`:
  Computes STFT magnitude and phase.
* `compute_istft(magnitude: np.ndarray, phase: np.ndarray, hop_length: Optional[int] = None, length: Optional[int] = None) -> np.ndarray`:
  Reconstructs time-domain signal from magnitude and phase using overlap-add.
* `apply_tpdf_dither(audio: np.ndarray, bits: int = 16) -> np.ndarray`:
  Applies Triangular Probability Density Function dither to prevent quantization distortion.
* `apply_phase_jitter(audio: np.ndarray, amount: float = 0.001) -> np.ndarray`:
  Applies all-pass micro-time phase jitter to break machine-deterministic periodicity.

---

## 4. Detectors (`nasuno.detectors`)

### `SunoWatermarkDetector`
```python
from nasuno.detectors.suno import SunoWatermarkDetector
```
Forensic detector targeting Suno AI high-frequency and harmonic watermarks.

#### Methods
* `detect(audio: np.ndarray, sr: int) -> DetectionResult`: Standardized protocol detection.
* `detect_watermark(audio: np.ndarray, sr: int) -> Dict[str, Any]`: Detailed metrics dictionary.

---

## 5. Removers (`nasuno.removers`)

### `IntegratedWatermarkRemover`
```python
from nasuno.core.pipeline import IntegratedWatermarkRemover
```
Unified high-level facade executing multi-pass detection, removal, and quality optimization.

#### Methods
* `process_file(input_path: str, output_path: str, processing_level: str = "balanced") -> ProcessingStats`:
  Executes full pipeline and returns telemetry stats.
