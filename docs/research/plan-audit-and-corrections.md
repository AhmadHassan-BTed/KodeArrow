# Master Evasion Plan: Audit, Corrections, and Architectural Refinement

> This document is a critical review of the [Master Evasion Plan v3](master-evasion-plan.md). It identifies factual errors, architectural flaws, and missing concerns. Each issue is documented with the correction, the research backing it, and the architectural fix. The master plan should be read in conjunction with this errata.

---

## I. Factual Errors Found

### ERROR 1: Phase Randomization Above 3 kHz Is NOT Unconditionally Safe

**What the plan says (Rule P1, Stage [7]):**
> "Above 2 kHz, phase can be freely randomized with zero audible consequence."
> "Above 3 kHz: full random phase replacement."

**Why this is wrong:**

Ohm's Acoustic Law and Grey & Gordon (1978) apply to **steady-state tones** -- sustained, unchanging harmonic complexes. They do NOT apply to transient signals. Phase coherence across frequency bins determines the **temporal shape** of transient events (attacks, consonants, drum hits). Randomizing phase across bins converts a sharp transient into diffuse noise-like energy spread over time.

Specifically:
- A snare drum hit has energy concentrated in a 1-2 ms burst. This burst requires phase coherence across all frequencies. Randomizing phase above 3 kHz would smear the high-frequency "crack" of the snare into a 20-50 ms wash.
- Vocal consonants (s, t, k, ch) are transient events above 3 kHz. Phase randomization would blur them.
- Piano attacks have phase-coherent hammer noise above 3 kHz. Randomization smears the attack.

**The corrected rule:**

Phase perception depends on **temporal context**, not just frequency:

| Condition | Phase Freedom | Research |
|-----------|-------------|----------|
| Steady-state, > 3 kHz | Full random | Ohm (1843), Plomp & Steeneken (1969) |
| Steady-state, 1-3 kHz | 0.5 rad max | Patterson (1987) |
| Steady-state, < 1 kHz | 0.26 rad max | Moore (2012) |
| **Transient frames, ANY frequency** | **Must preserve inter-bin phase relationships** | Grey & Gordon (1978), McAdams (1984) |

**Architectural fix:** Stage [7] must be split into two modes:
1. **Steady-state mode:** Apply full phase randomization above 3 kHz, controlled perturbation below. Active during sustained notes, chords, and held tones (where transient_map[frame] == False).
2. **Transient-preservation mode:** Preserve original phase during transient frames (where transient_map[frame] == True). Only apply slowly-varying group phase offset (same random offset to all bins in the frame, not independent random offsets per bin). This shifts the transient in time by < 1 sample without smearing its shape.

This split requires the **transient map** from the Content Intelligence Engine (already designed). The architecture already supports this -- the fix is in the algorithm, not the infrastructure.

---

### ERROR 2: Wiener Filter Is Weaker Than Claimed Against Neural Watermarks

**What the plan says (Stage [3]):**
> "Apply Wiener filter denoising... The Wiener filter removes both the added Gaussian noise AND the watermark residual."

**Why this is wrong (partially):**

2025 research (arxiv.org, confirmed by multiple studies) establishes that:
- Classical Wiener filtering is **less effective** than modern generative speech enhancement (SE) models at removing neural watermarks.
- Wiener filters struggle with non-stationary watermark signals and lack the learned feature extraction of deep models.
- Generative SE models that re-synthesize harmonic regions are "particularly destructive to neural watermarks."

The Wiener approach DOES work to some degree (watermark energy is reduced), but claiming it fully removes "most current neural watermarks" overstates its effectiveness. The taxonomy's own statement [R24] -- "generative speech enhancement after mild noise removes most current neural watermarks" -- refers to NEURAL speech enhancement, not classical Wiener filtering.

**The corrected approach -- tiered denoising:**

| Tier | Method | Effectiveness | Dependencies | Processing Level |
|------|--------|--------------|-------------|-----------------|
| **Tier 1** | Spectral subtraction (enhanced) | Moderate | numpy, scipy only | All levels |
| **Tier 2** | Wiener filter with oversubtraction | Good | numpy, scipy only | moderate+ |
| **Tier 3** | Multi-band Wiener with noise estimation | Better | numpy, scipy only | aggressive+ |
| **Tier 4** | Generative SE (optional, future) | Excellent | PyTorch, pretrained model | extreme (opt-in) |

For our zero-external-dependency core, Tiers 1-3 are available. The architecture should support Tier 4 as an optional plugin when PyTorch is available, but the plan should not claim Tier 1-3 effectiveness equals Tier 4.

**What this means concretely:**
- At `gentle` / `moderate`: Spectral subtraction + Wiener filtering will PARTIALLY attenuate neural watermarks (estimated 60-80% energy reduction). Combined with the other 18 stages (especially mel-domain removal, phase decorrelation, and statistical normalization), the cumulative effect may be sufficient.
- At `aggressive` / `extreme`: The optional generative SE tier would be the most reliable single-stage watermark destroyer. But it requires a pretrained model (~100 MB) and PyTorch.
- The plan should honestly state this limitation rather than overclaiming.

**Architectural fix:** `removers/neural_residual.py` should implement a `DenoiserStrategy` protocol:

```python
class DenoiserStrategy(Protocol):
    def denoise(self, audio: np.ndarray, sr: int, noise_psd: np.ndarray) -> np.ndarray: ...
```

With implementations:
- `SpectralSubtractionDenoiser` (always available)
- `WienerDenoiser` (always available)
- `MultibandWienerDenoiser` (always available)
- `GenerativeSEDenoiser` (optional, requires torch)

The pipeline selects the strongest available denoiser.

---

### ERROR 3: Mastering Camouflage Creates a NEW Fingerprint

**What the plan says (Stage [19]):**
> "Apply, in sequence: air-band shelf +0.2 dB, glue compression 1.1:1, true-peak limiting -0.3 dBTP."

**Why this is a risk:**

If every NaSuno-processed file has the EXACT SAME mastering chain parameters (same EQ frequency, same compression ratio, same threshold, same limiting ceiling), then "processed by NaSuno" becomes detectable by its processing signature. A forensic examiner analyzing 100 files and finding identical mastering parameters on all of them would immediately flag this as automated processing.

Real mastering engineers use different parameters for every song. A jazz ballad gets different EQ than a metal track. The mastering chain must vary.

**The corrected approach -- randomized mastering parameters:**

| Parameter | Fixed Value (v3, WRONG) | Randomized Range (CORRECTED) |
|-----------|------------------------|------------------------------|
| Air shelf frequency | 10 kHz | 8-14 kHz (uniform) |
| Air shelf gain | +0.2 dB | +0.1 to +0.4 dB (uniform) |
| Compression ratio | 1.1:1 | 1.05:1 to 1.2:1 (uniform) |
| Compression threshold | -18 dBFS | -22 to -14 dBFS (depends on input crest factor) |
| Compression attack | 20 ms | 10-40 ms (uniform) |
| Compression release | 150 ms | 80-250 ms (uniform) |
| True-peak ceiling | -0.3 dBTP | -0.5 to -0.1 dBTP (uniform) |

Additionally, the mastering chain order should occasionally vary (EQ before compression vs. compression before EQ -- both are common in real mastering).

**Architectural fix:** `core/mastering.py` should accept a `seed` parameter for deterministic randomization (reproducible results), but default to random. The randomization should be seeded from the audio content itself (hash of first 1024 samples) so the same input always produces the same parameters, but different inputs produce different parameters.

---

### ERROR 4: The Schroeder Masking Model Is Oversimplified

**What the psychoacoustics reference says:**
> ```
> T(z) = L_m - 27 + 0.37 * max(L_m - 40, 0) * (z - z_m)    [for z > z_m, upward]
> T(z) = L_m - 27 - (z_m - z) * 25                           [for z < z_m, downward]
> ```

**The issue:**

This is the Schroeder (1979) approximation of spreading function for a SINGLE masker. Real audio has DOZENS of simultaneous maskers. The combined masking threshold from multiple maskers is NOT the sum of individual masks -- it is approximately the `max` of individual masks (masking does not add linearly; it follows a power-law summation).

The MPEG psychoacoustic model (ISO 11172-3, Psychoacoustic Model 2) uses:
- Power-law summation: `T_combined = (sum(T_i^alpha))^(1/alpha)` where alpha approximately = 0.3
- This is less than linear summation but more than max -- two equal-level maskers provide about 3 dB more masking than one alone.

**Correction:** The perceptual engine should use power-law summation with alpha = 0.3, not simple max. This is a code-level fix, not an architectural change. The numbers in the psychoacoustics reference should note this limitation.

---

### ERROR 5: Cross-Correlation > 0.92 Is Too Loose for Some Content

**What the Quality Firewall says:**
> `cross_correlation: pearsonr(before, after) > 0.92`

**The issue:**

A correlation of 0.92 means 15% of the signal variance has been altered. For dense electronic music, this is inaudible. For a solo violin recording, a correlation drop to 0.92 would represent massive audible change.

**Correction:** The correlation threshold should be content-adaptive:

| Content Density | Correlation Threshold |
|----------------|----------------------|
| Dense (electronic, full band) | > 0.90 |
| Moderate (pop, rock, R&B) | > 0.94 |
| Sparse (solo instrument, acoustic, classical) | > 0.97 |

The Content Intelligence Engine already classifies density. This threshold should be derived from it.

---

### ERROR 6: 2-Cent Pitch Shift May Not Break Chromaprint

**What the plan says (Stage [16]):**
> "+2 cents global pitch shift... sufficient to alter Chromaprint/AcoustID fingerprint hashes."

**The issue:**

Chromaprint uses chroma features quantized to 12 semitone classes. A 2-cent shift is 1/50th of a semitone. The chroma quantization is MUCH coarser than 2 cents. The shift may or may not change the chroma vector depending on where the original pitch falls relative to the quantization boundary.

For most pitches, 2 cents will NOT change the chroma class. Only pitches that happen to fall within 2 cents of a chroma boundary will flip. The probability of this is approximately 4/100 = 4% per pitch. For a full song with hundreds of notes, some chromas will flip and some won't, producing a PARTIAL hash change.

**Correction:**
- 2-cent shift provides SOME hash disruption but not guaranteed full disruption.
- For guaranteed hash disruption, the minimum effective shift is approximately 10-15 cents (where the probability of at least one chroma flip per analysis window approaches 100%).
- However, 10-15 cents is near the pitch JND (5 cents for complex tones). This creates a tension.
- **Resolution:** Use 3 cents as the base shift (below JND for complex tones but above JND for isolated pure tones). Accept that hash disruption is probabilistic, not guaranteed. The stage should compute the ACTUAL Chromaprint delta and warn if similarity remains above 0.85.
- Combine with time-domain micro-stuttering (adding/removing 1-3 samples at zero-crossing points every 5-10 seconds) to create additional hash disruption without pitch change.

---

### ERROR 7: ENF Injection at -70 dBFS May Be Too Weak

**What the plan says (Stage [12]):**
> "Inject 50/60 Hz ENF at -70 dBFS."

**The issue:**

ENF analysis tools work by extracting the 50/60 Hz component and measuring its frequency drift over time. The minimum signal level for reliable ENF extraction depends on the recording's noise floor and the analysis window length. For a recording with a noise floor at -70 dBFS, an ENF injection at -70 dBFS has SNR = 0 dB in that band -- barely detectable by the analysis tool.

Typical ENF levels in real recordings range from -45 to -65 dBFS depending on the recording environment and equipment. Injecting at -70 dBFS may be too weak to be convincing to an ENF analysis tool.

**Correction:** Inject at `noise_floor - 3 dB` (3 dB above the measured noise floor in the 50 Hz band). This ensures the ENF is detectable by analysis tools while remaining below the overall noise floor. For typical AI audio with noise floor at -80 dBFS, this means injection at -77 dBFS. For AI audio with noise floor at -60 dBFS, injection at -57 dBFS.

---

## II. Architectural Flaws Found

### FLAW 1: ContentProfile Is a Monolithic God-Object

**The problem:** `ContentProfile` is a single dataclass with 17 fields. Every analyzer writes to it, every stage reads from it. This creates tight coupling: adding a new analyzer requires modifying the ContentProfile dataclass, and every stage that imports ContentProfile transitively depends on every analyzer.

**The fix -- Analyzer Registry with typed sub-profiles:**

```python
# Each analyzer produces its own typed result
class NoiseFloorAnalysis:
    floor_dbfs: float
    floor_per_band: np.ndarray

class TransientAnalysis:
    transient_map: np.ndarray
    onset_strengths: np.ndarray
    transient_density: float

class HarmonicAnalysis:
    f0_per_frame: np.ndarray
    harmonic_bins: dict
    inharmonicity: np.ndarray

# ... etc for each analyzer

# The ContentProfile is a container of optional sub-profiles
class ContentProfile:
    def get(self, analysis_type: Type[T]) -> Optional[T]: ...
    def set(self, analysis: T) -> None: ...

# Each analyzer is a Protocol
class ContentAnalyzer(Protocol):
    def analyze(self, audio: np.ndarray, sr: int) -> Any: ...
    
# Registration
engine.register_analyzer(NoiseFloorAnalyzer())      # produces NoiseFloorAnalysis
engine.register_analyzer(TransientAnalyzer())        # produces TransientAnalysis
engine.register_analyzer(HarmonicAnalyzer())         # produces HarmonicAnalysis
```

**Benefits:**
- Adding a new analyzer does not change ContentProfile's type signature.
- Stages declare which sub-profiles they need: `profile.get(TransientAnalysis)`.
- If a sub-profile is missing (analyzer not registered), the stage falls back to conservative defaults.
- Analyzers can be developed, tested, and deployed independently.

---

### FLAW 2: Fixed Pipeline Ordering Prevents Extensibility

**The problem:** The pipeline is a fixed 21-stage sequence. Adding a new stage requires editing the pipeline orchestrator and deciding where in the sequence it goes. Reordering requires changing multiple files.

**The fix -- DAG-based pipeline with declared dependencies:**

```python
class RemovalStage(Protocol):
    name: str
    depends_on: set[str]         # stages that must run before this one
    incompatible_with: set[str]  # stages that cannot run alongside this one
    
    def should_activate(self, profile: ContentProfile) -> bool: ...
    def remove(self, audio: np.ndarray, sr: int, **kwargs) -> tuple[np.ndarray, dict]: ...
```

The pipeline orchestrator:
1. Collects all registered stages.
2. Calls `should_activate()` on each with the ContentProfile.
3. Builds a DAG from the active stages' `depends_on` declarations.
4. Topologically sorts the DAG.
5. Executes stages in topological order, wrapping each in the Quality Firewall.

**Benefits:**
- Adding a new stage = registering a new class with its dependencies. Zero changes to the orchestrator.
- Stages can be developed by different people or in different sprints without coordination.
- Third-party stages can be plugged in via the same protocol.
- The pipeline can be visualized as a graph for debugging.

---

### FLAW 3: Perceptual Budget Assumes Stage Independence

**The problem:** The plan says:
> `remaining_budget[f, t] = initial_budget[f, t] - sum(consumed_by_stages_1_to_N[f, t])`

This assumes the masking profile is static. In reality, each stage CHANGES the signal, which CHANGES the masking profile. After Stage [5] attenuates an upsampler peak, the masking produced by that peak is reduced, which REDUCES the available budget for subsequent stages at nearby frequencies.

**The fix -- inter-stage budget recomputation:**

After each stage, recompute the masking model on the modified signal. This is more expensive (one additional STFT + masking computation per stage) but prevents the budget from being based on stale data.

```python
for stage in active_stages:
    budget = compute_budget(current_audio, sr)  # fresh computation
    result = firewall.guard(stage, current_audio, sr, budget)
    current_audio = result
```

---

### FLAW 4: Quality Firewall Lacks Frequency-Dependent Validation

**The problem:** The firewall checks global metrics (overall RMS, overall correlation, overall spectral centroid). But a stage could make a massive change in one frequency band while preserving the global metrics. Example: remove 20 dB at 3 kHz while adding 20 dB at 15 kHz. Global RMS is preserved. Global correlation might pass. But the 3 kHz change is clearly audible.

**The fix -- per-band validation:**

Add per-critical-band RMS checking to the firewall:

```python
for bark_band in range(1, 26):
    band_rms_before = compute_band_rms(audio_before, sr, bark_band)
    band_rms_after = compute_band_rms(audio_after, sr, bark_band)
    
    # Allow more change in insensitive bands
    max_change_db = iso226_tolerance[bark_band]  # e.g., 0.5 dB at 3 kHz, 6 dB at 15 kHz
    
    if abs(db(band_rms_after / band_rms_before)) > max_change_db:
        return ROLLBACK
```

This catches frequency-localized violations that global metrics miss.

---

### FLAW 5: No Version Control for Processing Parameters

**The problem:** If we later discover that a specific removal algorithm was too aggressive or had a bug, there is no way to know which version of parameters was used on a previously processed file.

**The fix:** Embed a processing manifest in the output file's metadata (in a private, non-AI-tagged field). The manifest contains:
- NaSuno version
- Active stages (by name)
- Strength parameters used per stage
- ContentProfile summary (density class, bandwidth, detected footprints)

---

### FLAW 6: Missing Separation Between "Signal Removers" and "Signal Injectors"

**The problem:** Some stages REMOVE information (watermark removal, peak attenuation) and some ADD information (noise injection, ENF injection, RIR convolution, variance injection). These have fundamentally different risk profiles:
- Removal stages can only make the signal simpler (lower energy in targeted regions). The risk is over-removal (creating silence or spectral holes).
- Injection stages add new signal content. The risk is the injection being audible or introducing its own detectable fingerprint.

**The fix -- split protocols:**

```python
class SignalSubtractor(Protocol):
    """Removes or attenuates signal components. Risk: over-removal."""
    def subtract(self, audio: np.ndarray, sr: int, budget: np.ndarray, **kwargs) -> tuple[np.ndarray, dict]: ...

class SignalInjector(Protocol):
    """Adds signal components. Risk: audibility of injected content."""
    def inject(self, audio: np.ndarray, sr: int, budget: np.ndarray, **kwargs) -> tuple[np.ndarray, dict]: ...
```

The Quality Firewall applies different validation for each.

---

### FLAW 7: The Minimum-Change Optimizer Binary Search Is Naive

**The problem:** The binary search assumes a monotonic relationship between strength and footprint removal. In reality, some removal algorithms have non-monotonic behavior.

**The fix:** Replace binary search with a sampled search:
1. Sample strengths at 0.2, 0.4, 0.6, 0.8, 1.0.
2. Measure footprint at each.
3. Find the LOWEST strength where footprint is below threshold.
4. If no strength achieves threshold, use 1.0 (maximum) and accept partial removal.
5. Refine with one additional binary search between the lowest passing strength and the next lower failing strength.

---

### FLAW 8: Missing Parallel Processing Integration

**The fix:** Parallelism at two levels:
1. **File-level parallelism:** Multiple files processed simultaneously (existing, works with new pipeline unchanged).
2. **Channel-level parallelism:** For stereo files, L and R channels can be processed in parallel for stages that operate independently per channel.

---

## III. Missing Concerns

### MISSING 1: Idempotency
Automatic via content-adaptive routing -- if no watermark is detected, watermark stages are skipped.

### MISSING 2: Graceful Degradation Under Extreme Content
Fallback behavior on edge cases (pure silence, extreme dynamic ranges).

### MISSING 3: Adaptive Processing Level Selector
Add `auto` processing level based on Content Intelligence density.

### MISSING 4: Test Coverage for Perceptual Claims
Build empirical validation suite for psychoacoustic claims.

### MISSING 5: Logging and Auditability
Per-file processing manifest and detailed execution log.

### MISSING 6: Mixed Content (AI + Human) Support
Architecture extensible to source-separation preprocessing.

---

## IV. Revised Architecture Summary

```
BEFORE (v3):                          AFTER (v4):
-----------                           -----------
Monolithic ContentProfile          -> Analyzer Registry + typed sub-profiles
Fixed 21-stage sequence            -> DAG with dependency declarations
Static perceptual budget           -> Recomputed between stages
Global-only quality checks         -> Per-critical-band + global checks
Single RemoverProtocol             -> Subtractor + Injector + PhaseModifier protocols
Fixed mastering parameters         -> Content-seeded randomized parameters
Phase randomization (all frames)   -> Transient-safe + steady-state modes
Single Wiener denoiser             -> Tiered denoiser strategy
Binary search optimizer            -> Sampled search with refinement
No logging                         -> Per-file processing manifest
No idempotency check               -> Automatic via content-adaptive routing
Manual processing level only       -> auto + manual override
```
