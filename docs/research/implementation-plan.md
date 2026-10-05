# NaSuno Web UI v3.0 — Definitive Implementation Plan

> Consolidated from: Enterprise Implementation Plan, UI & Analyzer Redesign Plan,
> Composite Knob Mapping, and Composite Knob Implementation Plan.
>
> **Rule**: Zero mocking. Zero code repetition. Every UI value comes from real DSP math.
> Every EngineConfig parameter (218 total) is accounted for — knob-driven, preset-toggled,
> or justified-fixed. The interface communicates AI footprint evasion, not DSP jargon.

---

## Table of Contents

1. [Architecture Overview](#1-architecture-overview)
2. [File Structure & Module Responsibilities](#2-file-structure--module-responsibilities)
3. [knob-registry.json — Single Source of Truth](#3-knob-registryjson--single-source-of-truth)
4. [Dual-Mode Panel System](#4-dual-mode-panel-system)
5. [14 Composite Knobs — Full Specification](#5-14-composite-knobs--full-specification)
6. [Complete Raw Parameter Registry (218 Parameters)](#6-complete-raw-parameter-registry-218-parameters)
7. [Info Icon Popover System](#7-info-icon-popover-system)
8. [Config I/O System](#8-config-io-system)
9. [Real Forensic Detection Engine](#9-real-forensic-detection-engine)
10. [Real DSP Processing Engine](#10-real-dsp-processing-engine)
11. [Accurate Spectrum Analyzer](#11-accurate-spectrum-analyzer)
12. [FL Studio Rack Aesthetic](#12-fl-studio-rack-aesthetic)
13. [Preset System](#13-preset-system)
14. [Bidirectional Sync Algorithm](#14-bidirectional-sync-algorithm)
15. [CLI Command & Config JSON Generation](#15-cli-command--config-json-generation)
16. [Implementation Phases](#16-implementation-phases)
17. [Validation Checklist](#17-validation-checklist)
18. [Purged Elements](#18-purged-elements)
19. [Parameter Coverage Audit](#19-parameter-coverage-audit)

---

## 1. Architecture Overview

```
┌──────────────────────────────────────────────────────────────┐
│  NASUNO v2.4          [PRESET ▼]   [BYPASS] [⚙️] [GH]       │
├──────────────────────────────────────────────────────────────┤
│  REAL-TIME FFT SPECTRUM ANALYZER (logarithmic, 20Hz–20kHz)  │
│  ┌──────────────────────────────────────────────────────────┐│
│  │  AnalyserNode → Canvas2D → real dBFS grid + curve       ││
│  │  Carrier markers at 15.5k, 17.5k, 19.5k with live dB    ││
│  └──────────────────────────────────────────────────────────┘│
│  FORENSIC TELEMETRY: real measured SNR, prominence, flatness │
├──────────────────────────────────────────────────────────────┤
│  ┌──────────────────────────────────────────────────────┐    │
│  │ [EVASION MODE] | [ADVANCED MODE] | [CONFIG I/O]     │    │
│  └──────────────────────────────────────────────────────┘    │
│                                                              │
│  EVASION MODE:  14 composite knobs in 4 modules              │
│    Each knob = one AI detection vector to defeat             │
│    ℹ️ info icon on every knob → popover with full details    │
│                                                              │
│  ADVANCED MODE: All 90 raw tunable params in collapsible     │
│    accordion sections by Python subsystem                    │
│    Each param shows parent composite knob                    │
│                                                              │
│  CONFIG I/O:  Download template | Import JSON | Export config│
│                                                              │
│  [▶ Play] [A/B] [Upload] [Export WAV] [Export Config]        │
│  $ nasuno clean input.wav --carrier-erase 65 --neural-scrub… │
└──────────────────────────────────────────────────────────────┘
```

### Data Flow

```
User uploads audio
  → AudioContext.decodeAudioData() → Float32Array PCM
  → SunoDetector.analyze(pcm, sr)       ← Real STFT + carrier SNR
  → StegoDetector.analyze(pcm, sr)      ← Real cepstral echo detection
  → SpectralAnalyzer.analyze(pcm, sr)   ← Real flatness + dynamics
  → Update forensic readout with REAL measured values
  → Connect AudioBufferSource → DSP chain → AnalyserNode → Canvas
  → Knob changes → composite mapper → Web Audio params (live)
  → Export → OfflineAudioContext → 16-bit PCM WAV download
```

---

## 2. File Structure & Module Responsibilities

```
docs/
├── index.html              ← Shell: tab bar, empty containers (zero inline knob HTML)
├── style.css               ← All styles (tokens, rack, knobs, panels, popovers, responsive)
├── knob-registry.json      ← Single source of truth: every knob's metadata, info, curves
├── app.js                  ← Entry: imports modules, DOMContentLoaded boot
├── modules/
│   ├── knob.js             ← FLKnob class (generic rotary — zero knowledge of what it controls)
│   ├── composite.js        ← Scaling curve engine (lerp, forward/reverse mapping)
│   ├── dsp.js              ← NaSunoDSP class (Web Audio chain + WAV export)
│   ├── analyzer.js         ← AudioMath, SunoDetector, StegoDetector, SpectralAnalyzer
│   ├── spectrum.js         ← Real-time logarithmic spectrum canvas renderer
│   ├── config-io.js        ← Config template generation, import, export, validation
│   ├── ui.js               ← Panel tabs, info popovers, preset dropdown, bypass toggle
│   └── registry.js         ← Loads knob-registry.json, generates all DOM, wires events
└── audio/
    ├── demo_cleaned.wav
    ├── demo_cleaned.ogg
    ├── demo_original.wav
    └── demo_original.ogg
```

### Module Dependency Graph

```
app.js (entry point)
  ├── registry.js ← knob-registry.json (fetch at boot)
  │     ├── knob.js         (instantiates FLKnob per registry entry)
  │     ├── composite.js    (wires scaling curves from registry data)
  │     └── ui.js           (generates info popovers, panel tabs)
  ├── dsp.js                (Web Audio chain — receives { notch1Q, shelfGain, outGain })
  ├── analyzer.js           (forensic math — pure functions, no DOM)
  ├── spectrum.js           (canvas renderer — reads from AnalyserNode)
  └── config-io.js          (JSON template/import/export — reads from registry)
```

### Zero Repetition Rules

| Principle | Implementation |
|---|---|
| Knob metadata in ONE place | `knob-registry.json` — HTML, JS, info tooltips, CLI all read from it |
| FLKnob is generic | Takes `{ min, max, step, default, unit }` from registry. No DSP knowledge |
| Scaling curves are data, not code | Each composite knob has `curves[]` in JSON. `composite.js` has ONE generic lerp evaluator |
| DOM is data-driven | `registry.js` reads JSON → generates all knob HTML, advanced inputs, info content |
| Presets are data | Stored in JSON. `applyPreset(key)` iterates registry, calls `knob.setValue()` |
| CLI generation is generic | Iterates all raw params from registry, builds `--flag value` for non-default values |

---

## 3. knob-registry.json — Single Source of Truth

Complete schema with example entries. The real file contains ALL entries.

```jsonc
{
  "version": "2.4",

  "compositeKnobs": [
    {
      "id": "carrierErase",
      "label": "CARRIER ERASE",
      "module": "watermarkErase",
      "moduleTitle": "WATERMARK ERASE",
      "moduleSubtitle": "Direct removal of embedded AI marks",
      "ring": "cyan",
      "min": 0, "max": 100, "step": 1, "default": 50,
      "unit": "%",
      "liveDSP": true,

      "info": {
        "title": "Carrier Erase",
        "defeats": "Ultrasonic carrier tone detection (15–20 kHz)",
        "description": "Suno and Udio embed inaudible tonal carriers at 15.5, 17.5, and 19.5 kHz. This knob controls the Q-factor of three notch filters that surgically remove these carriers.",
        "howItWorks": "Three IIR notch filters at known carrier frequencies. Higher = sharper notch = deeper suppression. Q scales from 4.0 (wide) to 30.0 (surgical).",
        "tradeoff": "Very high values may create narrow spectral holes. Quality Gate prevents this."
      },

      "curves": [
        { "target": "classical.carrier_notch_q",               "lo": 10.0, "hi": 60.0 },
        { "target": "classical.spectral_peak_threshold_factor", "lo": 4.5,  "hi": 2.5 },
        { "target": "classical.harmonic_filterbank_q",          "lo": 20.0, "hi": 65.0 },
        { "target": "__dsp__.notch1Q",                          "lo": 4.0,  "hi": 30.0 },
        { "target": "__dsp__.notch2Q",                          "lo": 3.4,  "hi": 25.5 },
        { "target": "__dsp__.notch3Q",                          "lo": 2.8,  "hi": 21.0 }
      ]
    }
    // ... 13 more composite knobs (full specs in Section 5)
  ],

  "rawParams": [
    {
      "key": "firewall.composite_bark_floor_db",
      "label": "Composite Bark Floor",
      "subsystem": "firewall",
      "subsystemTitle": "QUALITY FIREWALL",
      "parentComposite": "qualityGate",
      "min": 1.0, "max": 8.0, "step": 0.1, "default": 2.5,
      "unit": "dB",
      "info": "Maximum spectral deviation per Bark band before quality rollback."
    }
    // ... 89 more raw params (full specs in Section 6)
  ],

  "fixedParams": [
    {
      "key": "firewall.n_fft", "value": 2048,
      "reason": "STFT frame size — algorithm constant for spectral resolution"
    }
    // ... 116 more fixed params
  ],

  "presets": {
    "lowProfile":       { "name": "Low Profile",       "description": "Light evasion, max fidelity", "values": { ... } },
    "standardEvasion":  { "name": "Standard Evasion",  "description": "Balanced all vectors",        "values": { ... } },
    "deepClean":        { "name": "Deep Clean",        "description": "Strong multi-vector",          "values": { ... } },
    "fullScrub":        { "name": "Full Scrub",        "description": "Maximum destruction",          "values": { ... } }
  }
}
```

---

## 4. Dual-Mode Panel System

### Tab Bar
```html
<div class="panel-tabs">
  <button class="panel-tab active" data-panel="evasion">EVASION MODE</button>
  <button class="panel-tab" data-panel="advanced">ADVANCED MODE</button>
  <button class="panel-tab" data-panel="config">CONFIG I/O</button>
</div>
```

### Panel A: EVASION MODE (default)
14 composite knobs with FL Studio rotary dials, organized in 4 modules.
Each knob has an ℹ️ info button, readout, and per-vector evasion indicator.

### Panel B: ADVANCED MODE
All 90 tunable raw parameters in collapsible accordion sections organized by
Python subsystem. Each section header shows parent composite knob.
Grid of `<input type="number">` fields generated from `knob-registry.json`.

### Panel C: CONFIG I/O
- Download config template (JSON with all 218 params + comments)
- Import config via file upload or paste
- Export current config as `engine_knobs.json`

---

## 5. 14 Composite Knobs — Full Specification

### Module 1: WATERMARK ERASE (cyan rings)

| # | ID | Label | Defeats | Range | Live DSP |
|---|---|---|---|---|---|
| 1 | `carrierErase` | CARRIER ERASE | Ultrasonic carrier tones (15–20 kHz) | 0–100% | ✅ Notch Q |
| 2 | `strideRemove` | STRIDE REMOVE | Upsampler periodic comb artifacts | 0–100% | — |
| 3 | `stegoStrip` | STEGO STRIP | Cepstral echo & spread-spectrum hiding | 0–100% | — |
| 4 | `neuralScrub` | NEURAL SCRUB | Neural codec spectral residuals | 0–100% | — |

### Module 2: FINGERPRINT SCATTER (cyan rings)

| # | ID | Label | Defeats | Range | Live DSP |
|---|---|---|---|---|---|
| 5 | `spectralBlend` | SPECTRAL BLEND | Mel-frequency shape fingerprinting | 0–100% | — |
| 6 | `phaseScatter` | PHASE SCATTER | Phase coherence & correlation analysis | 0–100% | — |
| 7 | `statNormalize` | STAT NORMALIZE | Benford / entropy / quantization anomalies | 0–100% | — |
| 8 | `hashBreak` | HASH BREAK | AcoustID & Chromaprint fingerprint matching | 0–100% | — |

### Module 3: NATURALIZATION (green rings)

| # | ID | Label | Adds | Range | Live DSP |
|---|---|---|---|---|---|
| 9 | `roomInject` | ROOM INJECT | RIR reverb, ENF hum, mic jitter | 0–100% | — |
| 10 | `textureInject` | TEXTURE INJECT | LPC residual, bispectral saturation | 0–100% | — |
| 11 | `bandwidthHeal` | BANDWIDTH HEAL | Air band & brickwall cutoff fill | -6 to +6 dB | ✅ Shelf |

### Module 4: MASTERING & QUALITY (orange rings)

| # | ID | Label | Purpose | Range | Live DSP |
|---|---|---|---|---|---|
| 12 | `dynamicsNatural` | DYNAMICS | Compression profile & dither | 0–100% | — |
| 13 | `qualityGate` | QUALITY GATE | Bark-band tolerance before rollback | 1–6 dB | — |
| 14 | `outputGain` | OUTPUT | Master output level | -12 to +6 dB | ✅ Gain |

### Evasion Alignment Diagram

```
AI AUDIO DETECTION PIPELINE              NASUNO COMPOSITE KNOB
──────────────────────────────            ─────────────────────
1. Carrier scan (15-20 kHz)          ←── CARRIER ERASE
2. Upsample stride comb (172.3 Hz)   ←── STRIDE REMOVE
3. Echo hiding (cepstral quefrency)  ←── STEGO STRIP
4. Neural residual (spectral floor)  ←── NEURAL SCRUB
5. Mel-frequency fingerprint         ←── SPECTRAL BLEND
6. Phase coherence analysis          ←── PHASE SCATTER
7. Statistical anomalies             ←── STAT NORMALIZE
8. Acoustic hash matching            ←── HASH BREAK
9. Missing room/mic characteristics  ←── ROOM INJECT
10. Missing organic texture          ←── TEXTURE INJECT
11. Brickwall bandwidth cutoff       ←── BANDWIDTH HEAL
12. Dynamic range profile            ←── DYNAMICS
────────────────────────────
Quality gate prevents artifacts      ←── QUALITY GATE
```

### Complete Scaling Curves

All curves use generic lerp: `value = lo + (hi - lo) × (knobPosition / knobRange)`

**CARRIER ERASE (0–100%)**:
- `classical.carrier_notch_q`: 10.0 → 60.0
- `classical.spectral_peak_threshold_factor`: 4.5 → 2.5
- `classical.harmonic_filterbank_q`: 20.0 → 65.0
- `__dsp__.notch1Q`: 4.0 → 30.0
- `__dsp__.notch2Q`: 3.4 → 25.5 (notch1Q × 0.85)
- `__dsp__.notch3Q`: 2.8 → 21.0 (notch1Q × 0.70)

**STRIDE REMOVE (0–100%)**:
- `upsampler.comb_depth`: 0.01 → 0.15
- `upsampler.max_cut_db`: 3.0 → 12.0
- `upsampler.peak_threshold_db`: 3.5 → 1.0

**STEGO STRIP (0–100%)**:
- `classical.max_echo_cut_db`: 4.0 → 18.0
- `classical.echo_mad_multiplier`: 5.0 → 3.0
- `classical.echo_alpha_max`: 0.08 → 0.25
- `classical.spread_spectrum_threshold_mult`: 4.0 → 2.5
- `classical.qim_dither_base_scale`: 1e-5 → 5e-5
- `classical.qim_lattice_dither_max`: 2e-4 → 1e-3

**NEURAL SCRUB (0–100%)**:
- `neural_residual.tier`: 1 → 4 (stepped at 25/50/75/100%)
- `neural_residual.target_snr_db`: 45.0 → 30.0
- `neural_residual.ss_alpha`: 1.0 → 2.2
- `neural_residual.ss_beta`: 0.04 → 0.15
- `neural_residual.wiener_spectral_floor`: 0.12 → 0.03
- `neural_residual.micro_gain_deviation`: 0.001 → 0.005
- `noise_level`: 1e-5 → 5e-4

**SPECTRAL BLEND (0–100%)**:
- `mel_domain.mad_threshold`: 5.0 → 2.0
- `mel_domain.blend_ratio_max`: 0.10 → 0.50
- `mel_domain.min_linear_gain`: 0.20 → 0.05

**PHASE SCATTER (0–100%)**:
- `phase_decorrelate.inter_frame_variance_threshold`: 0.40 → 0.15
- `phase_decorrelate.transient_group_shift_max`: 0.02 → 0.10
- `phase_decorrelate.steady_state_dispersion_max`: 0.03 → 0.25
- `resynthesis.max_phase_dispersion`: 0.03 → 0.25
- `resynthesis.transient_shift_max`: 0.02 → 0.10
- `phase_variance`: 0.002 → 0.015

**STAT NORMALIZE (0–100%)**:
- `statistical.target_min_variance`: 0.08 → 0.18
- `statistical.spectral_flatness_floor`: 0.08 → 0.18
- `statistical.dither_floor_amp`: 5e-5 → 3e-4
- `statistical.benford_kl_threshold`: 0.08 → 0.03
- `statistical.benford_dither_strength`: 5e-5 → 2e-4
- `quantization.dither_amplitude`: 5e-5 → 5e-4
- `quantization.max_dither_clip`: 2e-4 → 1e-3
- `quantization.mode_spacing_fraction`: 0.20 → 0.45
- `distribution_noise_level`: 1e-5 → 5e-4

**HASH BREAK (0–100%)**:
- `hash_disrupt.base_cents`: 0.5 → 6.0
- `hash_disrupt.wow_depth_cents`: 0.17 → 2.0 (base × 0.33)
- `hash_disrupt.phase_jitter_amount`: 0.0001 → 0.0015
- `hash_disrupt.stutter_interval_sec`: 12.0 → 4.0
- `sync_disrupt.drift_depth`: 0.001 → 0.01
- `sync_disrupt.crop_min_samples`: 5 → 20 (int)
- `sync_disrupt.crop_max_samples`: 32 → 128 (int)
- `pipeline.frame_grid_jitter_max_samples`: 32 → 128 (int)
- `timing_stretch_range`: 0.001 → 0.01
- `timing_variation_range`: 0.001 → 0.008

**ROOM INJECT (0–100%)**:
- `environment.wet_mix`: 0.01 → 0.10
- `environment.rt60_sec`: 0.05 → 0.30
- `environment.enf_drift_sigma`: 0.002 → 0.010
- `environment.vocal_micro_jitter_percent`: 0.001 → 0.005

**TEXTURE INJECT (0–100%)**:
- `bispectral.cubic_coeff`: 0.005 → 0.04
- `bispectral.quintic_coeff`: 0.001 → 0.012
- `lpc_residual.pred_gain_threshold_db`: 5.0 → 2.0
- `lpc_residual.kurtosis_threshold`: 7.0 → 3.5
- `lpc_residual.micro_texture_rel_amp`: 0.004 → 0.02
- `disclosure.morse_corr_threshold`: 0.55 → 0.35
- `harmonic_distortion_amount`: 0.002 → 0.02
- `micro_dynamics_amount`: 0.0005 → 0.004

**BANDWIDTH HEAL (-6.0 to +6.0 dB)**:
- `__dsp__.shelfGain`: direct 1:1
- `mastering.air_gain_db_min`: max(0, value − 0.15)
- `mastering.air_gain_db_max`: max(0.05, value + 0.15)
- `bandwidth.comfort_noise_offset_db`: 24.0 → 16.0 (normalized over range)
- `bandwidth.rolloff_db_per_octave`: −18.0 → −6.0 (normalized over range)

**DYNAMICS (0–100%)**:
- `mastering.comp_ratio_min`: 1.02 → 1.15
- `mastering.comp_ratio_max`: 1.08 → 1.35
- `mastering.attack_ms_min`: 25.0 → 10.0
- `mastering.attack_ms_max`: 50.0 → 20.0
- `mastering.release_ms_min`: 120.0 → 60.0
- `mastering.release_ms_max`: 280.0 → 150.0
- `mastering.true_peak_ceiling_db_min`: −0.30 → −0.50
- `mastering.true_peak_ceiling_db_max`: −0.05 → −0.20
- `mastering.final_dither_amplitude`: 1e-5 → 5e-5

**QUALITY GATE (1.0–6.0 dB)**:
- `firewall.composite_bark_floor_db`: direct 1:1
- `firewall.structural_bark_floor_db`: value × 1.8
- `firewall.sparse_min_corr`: 0.985 → 0.88
- `firewall.sparse_max_rms_delta`: 0.015 → 0.07
- `firewall.sparse_max_lufs_delta`: 0.35 → 1.80
- `firewall.moderate_min_corr`: 0.965 → 0.86
- `firewall.moderate_max_rms_delta`: 0.025 → 0.08
- `firewall.moderate_max_lufs_delta`: 0.50 → 1.50
- `firewall.dense_min_corr`: 0.94 → 0.84
- `firewall.dense_max_rms_delta`: 0.03 → 0.12
- `firewall.dense_max_lufs_delta`: 0.60 → 2.0
- `firewall.composite_max_rms_delta`: 0.06 → 0.20
- `firewall.composite_max_lufs_delta`: 0.80 → 2.5
- `firewall.min_stereo_corr_sparse_moderate`: 0.98 → 0.90
- `firewall.min_stereo_corr_dense`: 0.96 → 0.88
- `firewall.max_phase_mag_delta_db`: 0.10 → 0.40
- `firewall.spectral_hole_margin_db`: 0.5 → 2.0
- `perceptual.alpha`: 0.15 → 0.60
- `pipeline.max_refinement_depth`: 3 → 1 (int)

**OUTPUT (-12.0 to +6.0 dB)**:
- `__dsp__.outGain`: direct 1:1

---

## 6. Complete Raw Parameter Registry (218 Parameters)

### Classification
- **🎛️ KNOB** (90): Driven by composite knob scaling curve
- **⚙️ PRESET** (11): Toggled by preset level selection
- **🔧 FIXED** (117): Structural constant with justification

### Top-Level EngineConfig (17 params)

| Parameter | Classification | Driven By |
|---|---|---|
| `processing_level` | ⚙️ PRESET | Preset selector |
| `filter_order` | ⚙️ PRESET | gentle=2, mod=2, agg=3, ext=4 |
| `filter_width_multiplier` | ⚙️ PRESET | gentle=0.5, mod=0.8, agg=1.0, ext=1.5 |
| `noise_level` | 🎛️ KNOB | `neuralScrub` |
| `skip_low_freq_threshold` | ⚙️ PRESET | gentle=300, mod=250, agg=200, ext=150 |
| `timing_stretch_range` | 🎛️ KNOB | `hashBreak` |
| `distribution_noise_level` | 🎛️ KNOB | `statNormalize` |
| `harmonic_distortion_amount` | 🎛️ KNOB | `textureInject` |
| `phase_variance` | 🎛️ KNOB | `phaseScatter` |
| `micro_dynamics_amount` | 🎛️ KNOB | `textureInject` |
| `timing_variation_range` | 🎛️ KNOB | `hashBreak` |
| `segment_overlap_ratio` | 🔧 FIXED | 50% Hann window overlap |
| `stft_size` | ⚙️ PRESET | gentle=1024, mod/agg=2048, ext=4096 |
| `enable_watermark_removal` | 🔧 FIXED | Core purpose — always true |
| `enable_pattern_normalization` | 🔧 FIXED | Required for stat norm |
| `enable_timing_variations` | 🔧 FIXED | Part of anti-hash chain |
| `enable_harmonic_adjustments` | ⚙️ PRESET | gentle=false, others=true |

### By Subsystem (Remaining 201 params)

| Subsystem | Total | 🎛️ | ⚙️ | 🔧 | Parent Composite |
|---|---|---|---|---|---|
| FirewallKnobs | 23 | 17 | 0 | 6 | `qualityGate` |
| PerceptualKnobs | 5 | 1 | 0 | 4 | `qualityGate` |
| MelDomainKnobs | 8 | 3 | 0 | 5 | `spectralBlend` |
| NeuralResidualKnobs | 10 | 6 | 0 | 4 | `neuralScrub` |
| SyncDisruptKnobs | 6 | 3 | 0 | 3 | `hashBreak` |
| UpsamplerKnobs | 9 | 3 | 0 | 6 | `strideRemove` |
| ClassicalKnobs | 20 | 8 | 1 | 11 | `carrierErase` + `stegoStrip` |
| PhaseDecorrelateKnobs | 5 | 3 | 0 | 2 | `phaseScatter` |
| ResynthesisKnobs | 5 | 2 | 1 | 2 | `phaseScatter` |
| StatisticalKnobs | 8 | 5 | 0 | 3 | `statNormalize` |
| QuantizationKnobs | 5 | 3 | 0 | 2 | `statNormalize` |
| BandwidthKnobs | 7 | 2 | 0 | 5 | `bandwidthHeal` |
| EnvironmentKnobs | 6 | 4 | 0 | 2 | `roomInject` |
| BispectralKnobs | 2 | 2 | 0 | 0 | `textureInject` |
| LPCResidualKnobs | 5 | 3 | 0 | 2 | `textureInject` |
| DisclosureKnobs | 5 | 1 | 0 | 4 | `textureInject` |
| HashDisruptKnobs | 6 | 5 | 0 | 1 | `hashBreak` |
| MasteringKnobs | 13 | 11 | 0 | 2 | `dynamicsNatural` + `bandwidthHeal` |
| PipelineKnobs | 9 | 2 | 2 | 5 | `qualityGate` + `hashBreak` |
| Detector/AnalyzerKnobs | 39 | 0 | 0 | 39 | (detection thresholds — calibrated) |

---

## 7. Info Icon Popover System

Every knob (composite and raw) has an ℹ️ button. Clicking it opens a popover.

### Composite Knob Popover Content (from `knob-registry.json`)

```
┌─────────────────────────────────────────────┐
│  CARRIER ERASE                          ✕   │
├─────────────────────────────────────────────┤
│  DEFEATS                                    │
│  Ultrasonic carrier tone detection          │
│  (15–20 kHz)                                │
│                                             │
│  DESCRIPTION                                │
│  Suno and Udio embed inaudible tonal        │
│  carriers at 15.5, 17.5, and 19.5 kHz.     │
│  This knob controls the Q-factor of three   │
│  notch filters that surgically remove them. │
│                                             │
│  HOW IT WORKS                               │
│  Three IIR notch filters at known carrier   │
│  frequencies. Higher = sharper = deeper.    │
│                                             │
│  TRADEOFF                                   │
│  Very high values may create narrow         │
│  spectral holes. Quality Gate prevents this.│
│                                             │
│  DRIVES 6 PARAMETERS                        │
│  • classical.carrier_notch_q: 10→60         │
│  • classical.spectral_peak_threshold: 4.5→2.5│
│  • classical.harmonic_filterbank_q: 20→65   │
│  • DSP notch1Q: 4→30                        │
│  • DSP notch2Q: 3.4→25.5                    │
│  • DSP notch3Q: 2.8→21                      │
└─────────────────────────────────────────────┘
```

### Raw Parameter Info (simpler)
```
┌─────────────────────────────────────────────┐
│  composite_bark_floor_db               ✕    │
│  Max spectral deviation per Bark band       │
│  before quality firewall triggers rollback. │
│  Parent: QUALITY GATE                       │
│  Range: 1.0 – 8.0 dB                       │
└─────────────────────────────────────────────┘
```

### Implementation (`ui.js`)
- Single shared popover element, repositioned per click
- Content populated from `knob-registry.json` via the loaded registry
- Clicking outside or pressing Escape closes it
- On mobile: popover becomes a bottom sheet

---

## 8. Config I/O System

### Template Download (`config-io.js`)
Generates complete `engine_knobs.json` with all 218 params, defaults,
and `_comment` fields per subsystem. User fills values and imports back.

### Import (`config-io.js`)
- File upload (`<input type="file" accept=".json">`)
- Paste JSON into textarea
- Validates against EngineConfig schema (warns on unknown keys, type mismatches)
- Applies values to raw param inputs → triggers reverse-mapping to composite knobs

### Export (`config-io.js`)
- Reads all 90 raw param values + 117 fixed values + 11 preset values
- Structures as nested JSON matching Python `EngineConfig` dataclass layout
- Downloads as `engine_knobs.json`
- CLI usage: `nasuno clean input.wav --config engine_knobs.json`

---

## 9. Real Forensic Detection Engine

Ported from `src/nasuno/detectors/suno.py` and `steganography.py`.

### AudioMath (Pure DSP Primitives)
| Function | Formula |
|---|---|
| `hannWindow(N)` | w[n] = 0.5(1 - cos(2πn/(N-1))) |
| `fft(re, im)` | Cooley-Tukey radix-2 in-place |
| `magnitudeSpectrum(segment, window)` | \|X[k]\| = √(re² + im²) |
| `stft(samples, nfft, hop)` | Overlapping windowed FFT frames |
| `spectralFlatness(frame)` | SFM = exp(mean(ln\|X\|²)) / mean(\|X\|²) |

### SunoDetector
- STFT with N=4096, hop=1024, Hann window
- Scan 3 carrier bands: 15–16 kHz, 17–18 kHz, 19–20 kHz
- Moving median spectral floor (k=±50 bins)
- Carrier SNR: 20·log10(peak / floor)
- Temporal stability: σ_E / μ_E (persistent carriers < 0.10)

### StegoDetector
- Real cepstrum: c[n] = IFFT(ln|FFT(x)|)
- Search 0.5–15 ms quefrency range
- MAD-based peak detection (threshold = 3.5×MAD)

### SpectralAnalyzer
- Average spectral flatness across frames
- Peak dBFS, RMS dBFS, Crest Factor

---

## 10. Real DSP Processing Engine

### Web Audio Filter Chain
```
Source → Notch₁(15.5kHz) → Notch₂(17.5kHz) → Notch₃(19.5kHz) → HighShelf(12kHz) → Gain → Analyser → Destination
```

| Node | Type | Controlled By |
|---|---|---|
| Notch 1 | BiquadFilterNode notch, f₀=15500 Hz | `carrierErase` → notch1Q |
| Notch 2 | BiquadFilterNode notch, f₀=17500 Hz | `carrierErase` → notch2Q |
| Notch 3 | BiquadFilterNode notch, f₀=19500 Hz | `carrierErase` → notch3Q |
| Air Shelf | BiquadFilterNode highshelf, f₀=12000 Hz | `bandwidthHeal` → shelfGain |
| Master Gain | GainNode | `outputGain` → dB-to-linear |
| Analyser | AnalyserNode, N=2048, smoothing=0.8 | Spectrum renderer |

### WAV Export
1. `OfflineAudioContext` matching file duration + sample rate
2. Same cascaded filter chain
3. Encode → 16-bit PCM WAV (DataView + Blob)
4. Trigger `<a download>` browser download

### Bypass Mode
All notch Q → 0.0001, shelf gain → 0 dB, master → 0 dB

---

## 11. Accurate Spectrum Analyzer

### Logarithmic Frequency Mapping
```
x(f) = W × log10(f / 20) / log10(20000 / 20)
```

### Grid Lines
- Frequency: 50, 100, 250, 500, 1k, 2k, 4k, 8k, 16k, 20k Hz
- Amplitude: +6, 0, −6, −12, −24, −36, −48, −60 dBFS

### Carrier Markers
Vertical dashed lines at 15.5k, 17.5k, 19.5k with real-time attenuation readout.

### Data Source
`AnalyserNode.getFloatFrequencyData()` — never synthetic data.
When no audio: flat −60 dBFS baseline with grid.

---

## 12. FL Studio Rack Aesthetic

### Design Tokens
| Token | Value | Usage |
|---|---|---|
| `--bg-space` | `#0b0d10` | Page background |
| `--rack-body` | `#16191f` | Main chassis |
| `--rack-panel` | `#1d2128` | Module panels |
| `--fl-orange` | `#ff7619` | Active preset, accent |
| `--fl-cyan` | `#00e5ff` | Spectrum, info tags |
| `--fl-green` | `#10f279` | Status OK |
| `--fl-red` | `#ff3344` | Detected carriers |

### Knob Rendering
- Brushed metal rotor: `radial-gradient` with highlight
- Concentric ring arc: SVG circle with `stroke-dasharray` (270° sweep)
- Indicator dot: 3×8px white rectangle, box-shadow glow
- Drag physics: vertical 200px = full range, scroll wheel fine, double-click reset

### What's NOT in the Design
- ❌ No spinning radar circle
- ❌ No `//`, `[]`, `01 :` formatting
- ❌ No `TRIPLE-ZERO EVASION VERIFIED`
- ❌ No `100% UNCONSTRAINED HUMAN MASTER`
- ❌ No `$ nasuno clean` CLI promo bar
- ❌ No `pip install nasuno` pill
- ❌ No neon bloom / excessive glow
- ❌ No hardcoded detection percentages
- ❌ No synthetic sine-wave spectrum

---

## 13. Preset System

| ID | Display | Description |
|---|---|---|
| `lowProfile` | Low Profile | Light evasion, max fidelity |
| `standardEvasion` | Standard Evasion | Balanced across all vectors |
| `deepClean` | Deep Clean | Strong multi-vector evasion |
| `fullScrub` | Full Scrub | Maximum footprint destruction |

### Preset Values (from `get_profile()` reverse-solved)

| Knob | Low Profile | Standard | Deep Clean | Full Scrub |
|---|---|---|---|---|
| `carrierErase` | 20% | 50% | 75% | 95% |
| `strideRemove` | 15% | 35% | 55% | 80% |
| `stegoStrip` | 20% | 45% | 65% | 85% |
| `neuralScrub` | 20% | 45% | 65% | 80% |
| `spectralBlend` | 25% | 40% | 60% | 80% |
| `phaseScatter` | 15% | 40% | 55% | 75% |
| `statNormalize` | 20% | 40% | 55% | 75% |
| `hashBreak` | 12% | 30% | 60% | 85% |
| `roomInject` | 15% | 35% | 55% | 75% |
| `textureInject` | 15% | 35% | 50% | 70% |
| `bandwidthHeal` | +0.5 dB | +0.25 dB | 0.0 dB | −0.5 dB |
| `dynamicsNatural` | 20% | 40% | 60% | 80% |
| `qualityGate` | 2.0 dB | 3.0 dB | 3.8 dB | 4.5 dB |
| `outputGain` | 0.0 dB | 0.0 dB | 0.0 dB | 0.0 dB |

---

## 14. Bidirectional Sync Algorithm

### Evasion → Advanced (forward)
When composite knob K is set to value V:
```
for each curve in K.curves:
    rawValue = lerp(curve.lo, curve.hi, normalize(V, K.min, K.max))
    update Advanced Mode input for curve.target
```

### Advanced → Evasion (reverse)
When raw param P is edited:
```
find composite knob K that drives P
for each curve in K.curves:
    expected = lerp(curve.lo, curve.hi, normalize(K.value, K.min, K.max))
    if |actual - expected| > tolerance:
        K.display = 'CUSTOM'
        return
K.value = reverseLearp(P.value, curve.lo, curve.hi) * K.range + K.min
```

When composite shows `CUSTOM`: readout shows "CUSTOM" + "Reset to Curve" button.

---

## 15. CLI Command & Config JSON Generation

### CLI Command (updates on every knob change)
```
nasuno clean input.wav \
  --level standard \
  --carrier-erase 65 \
  --neural-scrub 50 \
  --stride-remove 40 \
  --stego-strip 45 \
  --spectral-blend 40 \
  --phase-scatter 40 \
  --stat-normalize 40 \
  --hash-break 30 \
  --room-inject 35 \
  --texture-inject 35 \
  --bandwidth-heal 0.25 \
  --dynamics 40 \
  --quality-gate 3.0 \
  --output-gain 0.0
```

### Config JSON Export
```json
{
  "processing_level": "moderate",
  "firewall": { "composite_bark_floor_db": 3.0, ... },
  "neural_residual": { "tier": 2, "target_snr_db": 38.0, ... },
  ...
}
```
Usage: `nasuno clean input.wav --config exported_knobs.json`

---

## 16. Implementation Phases

### Phase 1: Foundation (modules/ directory)
1. Create `docs/modules/` directory
2. Extract `FLKnob` class → `modules/knob.js`
3. Create `modules/composite.js` — generic lerp, mapForward, mapReverse
4. Move `analyzer.js` → `modules/analyzer.js` (already complete)
5. Move `dsp.js` → `modules/dsp.js` (already complete)
6. Extract canvas renderer → `modules/spectrum.js`
7. Create `modules/ui.js` — tabs, popovers, dropdown, bypass
8. Create `modules/config-io.js` — template, import, export
9. Create `modules/registry.js` — JSON loader, DOM builder, wiring

### Phase 2: Knob Registry JSON
1. Create `docs/knob-registry.json` with complete schema
2. All 14 composite knobs with info + curves
3. All 90 raw params with metadata
4. All 117 fixed params with justifications
5. All 4 presets with values

### Phase 3: HTML Shell
1. Rewrite `index.html` as minimal shell (tab bar + containers)
2. All knob HTML generated by `registry.js` from JSON
3. Keep SEO meta tags, JSON-LD, fonts

### Phase 4: CSS Updates
1. Tab bar styles
2. Advanced panel accordion styles
3. Config I/O panel card styles
4. Info popover styles (positioned, dismissible)
5. ℹ️ button styles
6. `CUSTOM` badge styles
7. Responsive: 3-col → 2-col → 1-col

### Phase 5: app.js Entry Point
1. Import all modules
2. Boot: fetch registry JSON → registry.init() → wire everything
3. Audio loading, playback, forensic analysis
4. Bidirectional sync wiring
5. CLI command live update (debounced 200ms)

### Phase 6: Testing
1. All 14 composite knobs function (drag, wheel, shift-drag, double-click)
2. All 90 advanced raw params editable
3. Composite ↔ advanced sync works both directions
4. CUSTOM badge appears when raw param breaks curve
5. ℹ️ popovers show correct content for all knobs
6. Presets update both panels
7. Config template download → valid JSON
8. Config import → both panels update
9. Config export → valid EngineConfig JSON
10. Live DSP (Carrier Erase / Bandwidth Heal / Output) works
11. WAV export works with current DSP params
12. Forensic analysis shows real measured values
13. Spectrum analyzer shows real FFT data

### Phase 7: Commit & Deploy
1. `pytest` → 64/64 pass
2. `git add .`
3. `git commit -m "feat(web): v3.0 — dual-mode evasion knobs, config I/O, info popovers"`
4. `git push origin main` (pre-push validates)
5. GitHub Pages auto-deploys

---

## 17. Validation Checklist

- [ ] Upload `demo_original.wav` → carrier prominence > +5 dB at 17.5k/19.5k
- [ ] Upload `demo_cleaned.wav` → carrier prominence < 0 dB
- [ ] Toggle A/B → spectrum shows carrier spikes appear/disappear
- [ ] Drag CARRIER ERASE knob → live audible notch change
- [ ] CARRIER ERASE at 0% → carriers visible; at 100% → carriers suppressed
- [ ] Switch to Advanced Mode → all 90 params visible and editable
- [ ] Edit raw param → parent composite knob shows CUSTOM
- [ ] Click ℹ️ on any knob → popover with correct info from registry
- [ ] Apply preset → all 14 composite + all 90 raw params update
- [ ] Download config template → valid JSON with comments
- [ ] Import config JSON → both panels update correctly
- [ ] Export config → works with `nasuno clean --config`
- [ ] Export WAV → downloads valid 16-bit PCM WAV
- [ ] Bypass mode → all filters disabled
- [ ] CLI command updates on every knob change
- [ ] No `//`, `[]`, `MOCK`, `TRIPLE-ZERO` anywhere
- [ ] All detection values are real measured numbers
- [ ] No console errors
- [ ] 64/64 Python tests pass
- [ ] GitHub Pages deploys successfully

---

## 18. Purged Elements

| Purged | Replaced With |
|---|---|
| `MOCK SCANNER` | Real forensic detection engine |
| `TRIPLE-ZERO EVASION VERIFIED` | Per-knob evasion indicators |
| `100% UNCONSTRAINED HUMAN MASTER` | `Status: Watermark Not Detected` |
| `$ nasuno clean...` CLI promo | CLI command generator (reflects actual knob state) |
| `pip install nasuno` pill | Removed |
| Spinning radar circle | Clean vector LED + numeric readout |
| Fake `0.89 [DETECTED]` values | Real STFT-measured carrier SNR |
| Simulated sine spectrum | Real AnalyserNode FFT data |
| `//`, `[]`, `01 :` formatting | Clean professional labels |

---

## 19. Parameter Coverage Audit

| Category | Total | 🎛️ Knob | ⚙️ Preset | 🔧 Fixed | Uncontrolled |
|---|---|---|---|---|---|
| Top-level EngineConfig | 17 | 6 | 7 | 4 | **0** |
| FirewallKnobs | 23 | 17 | 0 | 6 | **0** |
| PerceptualKnobs | 5 | 1 | 0 | 4 | **0** |
| MelDomainKnobs | 8 | 3 | 0 | 5 | **0** |
| NeuralResidualKnobs | 10 | 6 | 0 | 4 | **0** |
| SyncDisruptKnobs | 6 | 3 | 0 | 3 | **0** |
| UpsamplerKnobs | 9 | 3 | 0 | 6 | **0** |
| ClassicalKnobs | 20 | 8 | 1 | 11 | **0** |
| PhaseDecorrelateKnobs | 5 | 3 | 0 | 2 | **0** |
| ResynthesisKnobs | 5 | 2 | 1 | 2 | **0** |
| StatisticalKnobs | 8 | 5 | 0 | 3 | **0** |
| QuantizationKnobs | 5 | 3 | 0 | 2 | **0** |
| BandwidthKnobs | 7 | 2 | 0 | 5 | **0** |
| EnvironmentKnobs | 6 | 4 | 0 | 2 | **0** |
| BispectralKnobs | 2 | 2 | 0 | 0 | **0** |
| LPCResidualKnobs | 5 | 3 | 0 | 2 | **0** |
| DisclosureKnobs | 5 | 1 | 0 | 4 | **0** |
| HashDisruptKnobs | 6 | 5 | 0 | 1 | **0** |
| MasteringKnobs | 13 | 11 | 0 | 2 | **0** |
| PipelineKnobs | 9 | 2 | 2 | 5 | **0** |
| Detector/AnalyzerKnobs | 39 | 0 | 0 | 39 | **0** |
| **TOTAL** | **218** | **90** | **11** | **117** | **0** |

**90 knob-driven + 11 preset-toggled + 117 justified-fixed = 218/218. Zero uncontrolled.**
